from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, schemas, database, auth

router = APIRouter()


@router.post(
    "/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 사용자 이름으로 사용자 검색
    db_user = crud.get_user_by_country_name(db, country_name=user.country_name)
    if db_user:
        # 이미 존재하는 사용자 예외 처리
        raise HTTPException(status_code=400, detail="User already exists")

    # 사용자 생성
    return crud.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(database.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # DB에서 사용자 인증
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 액세스 토큰 생성
    access_token = auth.create_access_token(data={"sub": user.country_name})
    return {"access_token": access_token, "token_type": "bearer"}
