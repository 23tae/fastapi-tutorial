from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_country_name(db: Session, country_name: str):
    # 사용자 이름으로 사용자 검색
    return (
        db.query(models.User).filter(models.User.country_name == country_name).first()
    )


def create_user(db: Session, user: schemas.UserCreate):
    # 비밀번호 해싱
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        country_name=user.country_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 비밀번호 검증
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, country_name: str, password: str):
    user = get_user_by_country_name(db, country_name)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete_all_users(db: Session):
    db.query(models.User).delete()
    db.commit()


def delete_user_by_id(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    return db.commit()
