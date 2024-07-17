from redis import Redis
import requests
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv
from urllib.parse import urljoin


load_dotenv()

emissions_api_url = os.getenv("CARBON_EMISSIONS_API_URL")
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

redis = Redis(host=redis_host, port=redis_port, db=0)

latest_emissions_api_url = urljoin(emissions_api_url, "latest")
day_emissions_api_url = urljoin(emissions_api_url, "history")


def fetch_and_cache_data():
    now = datetime.utcnow()
    current_hour = now.hour

    for country in [
        "KR",
        "US",
        "JP",
        "IN",
        "RU",
        "DE",
    ]:
        latest_response = requests.get(f"{latest_emissions_api_url}?country={country}")
        hourly_response = requests.get(f"{day_emissions_api_url}?country={country}")

        if latest_response.status_code == 200:
            redis.set(
                f"latest_{country}_{current_hour}", latest_response.json(), ex=3600
            )

        if hourly_response.status_code == 200:
            redis.set(
                f"hourly_{country}_{current_hour}", hourly_response.json(), ex=3600
            )


scheduler = AsyncIOScheduler()
scheduler.add_job(fetch_and_cache_data, "cron", minute=0)
scheduler.start()
