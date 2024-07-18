from fastapi import APIRouter, HTTPException
import datetime
import os
from redis import Redis
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

redis = Redis(host=redis_host, port=redis_port, db=0)


@router.get("/emissions")
def get_carbon_emissions():
    now = datetime.datetime.utcnow()
    current_hour = now.hour

    emissions_data = redis.get(f"emissions_{current_hour}")

    if emissions_data:
        emissions_data = json.loads(emissions_data)
        return emissions_data
    else:
        raise HTTPException(status_code=404, detail="Emissions data not found")
