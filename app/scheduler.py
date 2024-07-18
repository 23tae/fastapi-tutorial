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
    now = datetime.utcnow()
    current_hour = now.hour
    redis.set(f"emissions_{current_hour}", json.dumps(world_emissions), ex=7200)


def calculate_change_rate(earliest_emissions, latest_emissions):
    return round((latest_emissions - earliest_emissions) / earliest_emissions, 4) * 100


def parse_emissions_response(hourly_response):
    hourly_data = hourly_response.get("history", [])

    earliest_emissions = None
    latest_emissions = None

    if hourly_data:
        valid_entries = [
            entry for entry in hourly_data if entry.get("carbonIntensity") is not None
        ]

        if valid_entries:
            earliest_emissions = valid_entries[0].get("carbonIntensity")
            latest_emissions = valid_entries[-1].get("carbonIntensity")

    change_rate = calculate_change_rate(earliest_emissions, latest_emissions)

    return latest_emissions, change_rate


def is_data_exist() -> bool:
    now = datetime.utcnow()
    current_hour = now.hour
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
        hourly_response = requests.get(f"{emissions_api_url}?country={country_code}")

        if hourly_response.status_code == 200:
            try:
                data = hourly_response.json()  # Parse JSON response
                latest_emissions, change_rate = parse_emissions_response(data)
                country_emissions = {
                    "country": country_code,
                    "latest_emissions": latest_emissions,
                    "change_rate": change_rate,
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
    scheduler.add_job(fetch_and_cache_data, "cron", minute=0)
    scheduler.start()


# 독립 실행 시만 동작하게 함
if __name__ == "__main__":
    asyncio.run(start_scheduler())
