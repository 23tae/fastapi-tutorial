from redis import Redis
import requests
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv
from urllib.parse import urljoin
import json


load_dotenv()

emissions_api_url = os.getenv("CARBON_EMISSIONS_API_URL")
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

redis = Redis(host=redis_host, port=redis_port, db=0)

hourly_emissions_api_url = urljoin(emissions_api_url, "history")


def set_redis(world_emissions: dict):
    now = datetime.utcnow()
    current_hour = now.hour
    redis.set(f"emissions_{current_hour}", json.dump(world_emissions), ex=7200)


def calculate_change_rate(earliest_emissions, latest_emissions):
    return (latest_emissions - earliest_emissions) / earliest_emissions * 100


def parse_emissions_response(hourly_response):
    hourly_data = hourly_response.get("history")
    earliest_emissions = hourly_data[0].get("carbonIntensity")
    latest_emissions = hourly_data[-1].get("carbonIntensity")
    change_rate = calculate_change_rate(earliest_emissions, latest_emissions)
    return latest_emissions, change_rate


def fetch_and_cache_data():
    world_emissions = []

    for country_code in [
        "KR",
        "US",
        "JP",
        "IN",
        "RU",
        "DE",
    ]:
        hourly_response = requests.get(
            f"{hourly_emissions_api_url}?country={country_code}"
        )

        if hourly_response.status_code == 200:
            latest_emissions, change_rate = parse_emissions_response(hourly_response)
            country_emissions = {
                "country": country_code,
                "latest_emissions": latest_emissions,
                "change_rate": change_rate,
            }
            world_emissions.append(country_emissions)
    set_redis(world_emissions)


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_cache_data, "cron", minute=0)
    scheduler.start()

    # 스케줄러를 실행하고 계속 유지함
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_forever()


# 독립 실행 시만 동작하게 함
if __name__ == "__main__":
    start_scheduler()
