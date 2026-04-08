from sqlalchemy import Column, Float, Integer, String

from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(120), nullable=False, index=True)
    street = Column(String(255), nullable=True)
    city = Column(String(120), nullable=True, index=True)
    state = Column(String(120), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(120), nullable=True, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
