from redis import Redis
import requests
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()

emissions_api_url = os.getenv("CARBON_EMISSIONS_API_URL")
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

redis = Redis(host=redis_host, port=redis_port, db=0)


def set_redis(world_emissions: dict):
    # 현재 시간을 키로 Redis에 데이터 저장
    now = datetime.utcnow()
    current_hour = now.hour
    redis.set(f"emissions_{current_hour}", json.dumps(world_emissions), ex=7200)


def parse_emissions_response(hourly_response):
    hourly_data = hourly_response.get("history", [])

    earliest_emissions = None
    latest_emissions = None

    if hourly_data:
        # 유효한 배출량 데이터만 필터링
        valid_entries = [
            entry for entry in hourly_data if entry.get("carbonIntensity") is not None
        ]

        if valid_entries:
            earliest_emissions = valid_entries[0].get("carbonIntensity")
            latest_emissions = valid_entries[-1].get("carbonIntensity")

    # 배출량 변화량 계산
    change_amount = latest_emissions - earliest_emissions

    return latest_emissions, change_amount


def is_data_exist() -> bool:
    now = datetime.utcnow()
    current_hour = now.hour
    # 현재 시간의 데이터가 Redis에 존재하는지 확인
    return redis.exists(f"emissions_{current_hour}")


def fetch_and_cache_data():

    if is_data_exist():
        return

    world_emissions = []

    for country_code in [
        "KR",
        "US",
        "JP",
        "IN",
        "RU",
        "DE",
    ]:
        hourly_response = requests.get(f"{emissions_api_url}?zone={country_code}")

        if hourly_response.status_code == 200:
            try:
                data = hourly_response.json()  # Parse JSON response
                latest_emissions, change = parse_emissions_response(data)
                country_emissions = {
                    "country": country_code,
                    "latest_emissions": latest_emissions,
                    "change": change,
                }
                world_emissions.append(country_emissions)
            except ValueError as e:
                print(f"Error parsing JSON: {e}")
        else:
            print("open api error")
    set_redis(world_emissions)


async def start_scheduler():
    fetch_and_cache_data()
    scheduler = AsyncIOScheduler()
    # 매 정각에 데이터 가져오기 작업 예약
    scheduler.add_job(fetch_and_cache_data, "cron", minute=0)
    scheduler.start()


if __name__ == "__main__":
    asyncio.run(start_scheduler())
