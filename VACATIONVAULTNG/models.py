from sqlalchemy import (
    Boolean, Column, Integer,
    String, Text, Float, ForeignKey,
    DateTime, JSON
    # Numeric
)
from database import Base
from datetime import datetime

class Property_Listings(Base):
    __tablename__ = "Property_Listings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    listing_id = Column(String(15), unique=True, index=True)

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    property_type = Column(Text, nullable=False)

    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    max_guests = Column(Integer, nullable=False)

    weeks_per_year = Column(Integer, nullable=False)
    price = Column(Text)
    original_price = Column(Text)
    year_built = Column(Integer)
    # seller_id = Column(Text)
    # featured = Column(Boolean, default=False)
    status = Column(Text, default="active")  # "active/non-active"
    images = Column(JSON, nullable=True, default=list)  # to contain list of url to images of a property

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
