from fastapi import APIRouter, HTTPException, Depends
import datetime
import os
from redis import Redis
import json
from dotenv import load_dotenv
from ..auth import get_current_user

load_dotenv()

router = APIRouter()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

redis = Redis(host=redis_host, port=redis_port, db=0)


@router.get("/emissions")
def get_carbon_emissions(current_user: str = Depends(get_current_user)):
    now = datetime.datetime.utcnow()
    current_hour = now.hour

    # Redis에서 최근에 저장된 배출량 데이터 가져오기
    emissions_data = redis.get(f"emissions_{current_hour}")

    if emissions_data:
        emissions_data = json.loads(emissions_data)
        return emissions_data
    else:
        # 데이터가 없을 때 예외 처리
        raise HTTPException(status_code=404, detail="Emissions data not found")
