# Carbon Emissions Server

## 설명

탄소 배출권 거래 서비스의 서버입니다. FastAPI로 구축되었으며, 사용자 인증, 탄소 배출량 조회 및 업데이트 기능을 제공합니다.

## 사전 준비

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
alembic revision --autogenerate && alembic upgrade head
```

### 서버 실행

```shell
uvicorn app.main:app --reload
```

## API 엔드포인트

### 인증

POST `/token`: JWT 토큰을 발급합니다.

### 사용자

POST `/users/`: 새로운 사용자를 생성합니다.

GET `/users/all`: 모든 사용자를 조회합니다.

GET `/users/{user_id}`: ID로 사용자를 조회합니다.

DELETE `/users/all`: 모든 사용자를 삭제합니다.

DELETE `/users/{user_id}`: ID로 사용자를 삭제합니다.

### 탄소 배출

GET `/emissions/`: 현재 탄소 배출 데이터를 조회합니다.

## 정기 작업

서버는 외부 API에서 탄소 배출 데이터를 가져와 Redis에 캐싱하는 작업을 매시간 수행합니다.