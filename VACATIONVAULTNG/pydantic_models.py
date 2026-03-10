from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class NEW_PROPERTY_LISTING_PYDANTIC(BaseModel):
    title: str = Field(examples=["2bdrm Block of Flats in Horizon Cyberville, Ikate-Elegushi for rent"])
    description: str = Field(examples=["A nice 2 bedroom in a serene environment of Lekki just off the coastal road."])
    location: str = Field(examples=["Horizon Cyberville estate off Coastal Road, Ikate Lekki"])
    property_type: str = Field(examples=["Block of Flats"])
    bedrooms: int = Field(examples=["2"])
    bathrooms: int = Field(examples=["2"])
    max_guests: int = Field(examples=["3"])
    weeks_per_year: int = Field(examples=["52"])
    price: str = Field(examples=["450000"])
    original_price: str = Field(examples=["510000"])
    year_built: int = Field(examples=["2025"])
    status: str = Field(examples=["non-active"])

class UPDATE_PROPERTY_LISTING_PYDANTIC(BaseModel):
    property_id: str = Field(examples=["2Y-ID-NCLJ5NAU"])
    title: str = Field(examples=["2bdrm Block of Flats in Horizon Cyberville, Ikate-Elegushi for rent"])
    description: str = Field(examples=["A nice 2 bedroom in a serene environment of Lekki just off the coastal road."])
    location: str = Field(examples=["Horizon Cyberville estate off Coastal Road, Ikate Lekki"])
    property_type: str = Field(examples=["Block of Flats"])
    bedrooms: int = Field(examples=["2"])
    bathrooms: int = Field(examples=["2"])
    max_guests: int = Field(examples=["3"])
    weeks_per_year: int = Field(examples=["52"])
    price: str = Field(examples=["450000"])
    original_price: str = Field(examples=["510000"])
    year_built: int = Field(examples=["2025"])
    status: str = Field(examples=["active"])
