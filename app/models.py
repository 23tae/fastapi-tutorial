from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CarbonEmissions(Base):
    __tablename__ = "carbon_emissions"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    emissions = Column(Float, nullable=False)
    emissions_change = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
