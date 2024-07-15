# Carbon Emissions Server

## Description

탄소 배출권 거래 서비스의 서버입니다.

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
pip3 install -r requirements.txt
```

- PostgreSQL 설치

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
alembic revision --autogenerate -m "Initial migration"
```

```shell
alembic upgrade head
```

### 서버 실행

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
