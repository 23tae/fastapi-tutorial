# FastAPI Tutorial

## Description

탄소 배출권 거래 서비스의 서버입니다. FastAPI로 구축되었으며, 사용자 인증, 탄소 배출량 조회 및 업데이트 기능을 제공합니다.

## Prerequisite

- 가상환경 생성

```shell
 python3 -m venv .venv
```

- 가상환경 활성화

```shell
source ./.venv/bin/activate
```

- 패키지 설치

```shell
pip install -r requirements.txt
```

- PostgreSQL 설치 및 실행
- Redis 설치 및 실행

## Usage

### 데이터베이스

- PostgreSQL shell 접속

```shell
psql -U your_username
```

- 데이터베이스 생성

```SQL
CREATE
DATABASE your_dbname;
```

- Alembic 마이그레이션 적용

```shell
alembic revision --autogenerate && alembic upgrade head
```

### 서버 실행

```shell
uvicorn app.main:app --reload
```

## API

http://localhost:8000/docs

### auth

- POST `/register`: 새로운 사용자를 생성합니다.

- POST `/login`: 로그인 후 JWT 토큰을 발급합니다.

### user

- GET `/users/all`: 모든 사용자를 조회합니다.

- GET `/users/{user_id}`: ID로 사용자를 조회합니다.

- DELETE `/users/all`: 모든 사용자를 삭제합니다.

- DELETE `/users/{user_id}`: ID로 사용자를 삭제합니다.

### emissions

GET `/emissions`: 최근 탄소 배출량 데이터를 조회합니다.
