from VACATIONVAULTNG import app
from fastapi import (HTTPException, status)
from VACATIONVAULTNG.routes import db_dependency
from VACATIONVAULTNG.models import (Property_Listings)
from VACATIONVAULTNG.pydantic_models import (NEW_PROPERTY_LISTING_PYDANTIC)

import random, secrets, string

base_url = "/vacation/vault/ng"


@app.post(base_url+"/property/listing/new", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.post(base_url+"/property/listing/new/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def create_property_listing(pyd_data:NEW_PROPERTY_LISTING_PYDANTIC, db: db_dependency):
    title = pyd_data.title
    description = pyd_data.description
    location = pyd_data.location
    property_type = pyd_data.property_type
    bedrooms = pyd_data.bedrooms
    bathrooms = pyd_data.bathrooms
    max_guests = pyd_data.max_guests
    weeks_per_year = pyd_data.weeks_per_year
    price = pyd_data.price
    original_price = pyd_data.original_price
    year_built = pyd_data.year_built
    status = pyd_data.status

    chars = string.ascii_uppercase + string.digits
    listing_id = ''.join(random.choices(chars, k=2)) + "-ID-" + ''.join(random.choices(chars, k=8))

    new_listing = Property_Listings(
        listing_id=listing_id,
        title=title,
        description=description,
        location=location,
        property_type=property_type,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        max_guests=max_guests,
        weeks_per_year=weeks_per_year,
        price=price,
        original_price=original_price,
        year_built=year_built,
        status=status
    )
    db.add(new_listing)
    db.commit()

    get_property_listing = db.query(Property_Listings).filter(
        Property_Listings.listing_id == listing_id).first()

    property_listing = get_property_listing.__dict__
    property_listing.pop("id")

    return {
        "statusCode": 200,
        "message": "success",
        "data": property_listing
    }
