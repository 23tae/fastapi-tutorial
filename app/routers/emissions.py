from fastapi import APIRouter, Depends, HTTPException
import requests
from ..dependencies import get_current_user
from .. import schemas

router = APIRouter()


@router.get("/emissions/{country}")
def read_emissions(
    country: str, current_user: schemas.User = Depends(get_current_user)
):
    response = requests.get(f"https://api.example.com/emissions/{country}")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to fetch emissions data"
        )
    return response.json()
