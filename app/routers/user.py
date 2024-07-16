from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, auth

router = APIRouter()


# 테스트
@router.get("/user/all", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(database.get_db)):
    return crud.get_all_users(db)


@router.get("/user", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):

    user = crud.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/user/all")
def delete_all_users(db: Session = Depends(database.get_db)):
    return crud.delete_all_users(db)


@router.delete("/user")
def delete_user_by_id(user_id: int, db: Session = Depends(database.get_db)):

    user = crud.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user_by_id(db, id)
