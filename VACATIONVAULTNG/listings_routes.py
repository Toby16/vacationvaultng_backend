from VACATIONVAULTNG import app
from fastapi import (HTTPException, status, UploadFile, File, Form)
from VACATIONVAULTNG.routes import db_dependency
from VACATIONVAULTNG.helper import upload_property_image
from VACATIONVAULTNG.models import (Property_Listings)
from VACATIONVAULTNG.pydantic_models import (NEW_PROPERTY_LISTING_PYDANTIC,
    UPDATE_PROPERTY_LISTING_PYDANTIC, GET_PROPERTY_LISTING_PYDANTIC,
    PAGINATION_REQUEST_PYDANTIC, SEARCH_PROPERTY_LISTING_PYDANTIC)

import random, secrets, string
from math import ceil
from sqlalchemy import case, func, desc, or_
from typing import List

base_url = "/vacation/vault/ng"


@app.post(base_url+"/property/listing/new", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.post(base_url+"/property/listing/new/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def create_property_listing(
    pyd_data:NEW_PROPERTY_LISTING_PYDANTIC,
    images: List[UploadFile] = File(...),
db: db_dependency):
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

    image_urls = []
    for image in images:
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail=f"{image.filename} is not an image"
            )
        image_url = upload_property_image(image)
        image_urls.append(image_url)

    

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
        status=status,
        images=image_urls
    )
    db.add(new_listing)
    db.commit()

    get_property_listing = db.query(Property_Listings).filter(
        Property_Listings.listing_id == listing_id).first()

    property_listing = get_property_listing.__dict__
    property_listing.pop("id")
    property_listing.pop("_sa_instance_state", None)

    return {
        "statusCode": 200,
        "message": "success",
        "data": property_listing
    }


@app.post(base_url+"/property/listing/update", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.post(base_url+"/property/listing/update/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def update_property_listing(pyd_data:UPDATE_PROPERTY_LISTING_PYDANTIC, db: db_dependency):
    property_listing_id = pyd_data.property_id

    check_listing_id = db.query(Property_Listings).filter(
        Property_Listings.listing_id == property_listing_id).first()
    if check_listing_id is None:
        raise HTTPException(
            status_code=404,
            detail="property does not exist!"
        )

    if pyd_data.title is not None:
        check_listing_id.title=pyd_data.title
    if pyd_data.description is not None:
        check_listing_id.description=pyd_data.description
    if pyd_data.location is not None:
        check_listing_id.location=pyd_data.location
    if pyd_data.property_type is not None:
        check_listing_id.property_type=pyd_data.property_type
    if pyd_data.bedrooms is not None:
        check_listing_id.bedrooms=pyd_data.bedrooms
    if pyd_data.bathrooms is not None:
        check_listing_id.bathrooms=pyd_data.bathrooms
    if pyd_data.max_guests is not None:
        check_listing_id.max_guests=pyd_data.max_guests
    if pyd_data.weeks_per_year is not None:
        check_listing_id.weeks_per_year=pyd_data.weeks_per_year
    if pyd_data.price is not None:
        check_listing_id.price=pyd_data.price
    if pyd_data.original_price is not None:
        check_listing_id.original_price=pyd_data.original_price
    if pyd_data.year_built is not None:
        check_listing_id.year_built=pyd_data.original_price
    if pyd_data.status is not None:
        check_listing_id.status=pyd_data.status

    db.commit()
    db.refresh(check_listing_id)

    get_property_listing = db.query(Property_Listings).filter(
        Property_Listings.listing_id == property_listing_id).first()
    property_listing = get_property_listing.__dict__
    property_listing.pop("id")

    return {
        "statusCode": 200,
        "message": "success",
        "data": property_listing
    }


ITEMS_PER_PAGE = 10
@app.post(base_url+"/property/listing/browse", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.post(base_url+"/property/listing/browse/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def browse_property_listings(pyd_data: PAGINATION_REQUEST_PYDANTIC, db:db_dependency):
    try:
        page = max(pyd_data.page, 1)  # prevent page 0 or negative
        offset = (page - 1) * ITEMS_PER_PAGE

        # Get total count (for frontend pagination UI)
        total_items = db.query(Property_Listings).count()
        total_pages = ceil(total_items / ITEMS_PER_PAGE)
    
        if (page > total_pages) and (total_pages != 0):
            page = total_pages

    
        retrieve_all_listings = db.query(
            Property_Listings.listing_id,
            Property_Listings.title,
            Property_Listings.description,
            Property_Listings.location,
            Property_Listings.property_type,
            Property_Listings.bedrooms,
            Property_Listings.bathrooms,
            Property_Listings.max_guests,
            Property_Listings.weeks_per_year,
            Property_Listings.price,
            Property_Listings.original_price,
            Property_Listings.year_built,
            Property_Listings.status,
            Property_Listings.images,
            Property_Listings.created_at,
            Property_Listings.updated_at
        ).order_by(
            Property_Listings.id.desc(),
            Property_Listings.created_at.desc()
        ).offset(offset).limit(ITEMS_PER_PAGE).all()

        data = {
            "page": page,
            "per_page": ITEMS_PER_PAGE,
            "total_items": total_items,
            "total_pages": total_pages,
            "data": [row._asdict() for row in retrieve_all_listings]
        }

        return data
    except Exception as e:
        raise HTTPException(
            statusCode=400,
            detail=str(e)
        )


@app.post(base_url+"/property/listing/get", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.post(base_url+"/property/listing/get/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def retrieve_property_listing(pyd_data: GET_PROPERTY_LISTING_PYDANTIC, db: db_dependency):
    property_listing_id = pyd_data.property_id
    check_listing_id = db.query(Property_Listings).filter(
        Property_Listings.listing_id == property_listing_id).first()
    if check_listing_id is None:
        raise HTTPException(
            status_code=404,
            detail="property does not exist!"
        )
    property_listing = check_listing_id.__dict__
    property_listing.pop("id")

    return {
        "statusCode": 200,
        "message": "success",
        "data": property_listing
    }


@app.delete(base_url+"/property/listing/delete", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.delete(base_url+"/property/listing/delete/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def delete_property_listing(pyd_data: GET_PROPERTY_LISTING_PYDANTIC, db: db_dependency):
    property_listing_id = pyd_data.property_id
    check_listing_id = db.query(Property_Listings).filter(
        Property_Listings.listing_id == proeprty_listing_id).first()
    if check_listing_id is None:
        raise HTTPException(
            status_code=404,
            detail="property does not exist!"
        )
    db.delete(check_listing_id)
    db.commit()

    return {
        "statusCode": 200,
        "message": "[{}] deleted successfully".format(property_listing_id)
    }

@app.post(base_url+"/property/listing/search", status_code=status.HTTP_200_OK, tags=["Property Listing"])
@app.post(base_url+"/property/listing/search/", status_code=status.HTTP_200_OK, tags=["Property Listing"])
def search_property_listing(pyd_data: SEARCH_PROPERTY_LISTING_PYDANTIC, db: db_dependency):
    search_by = pyd_data.search_by
    search_input = pyd_data.search_input

    search_range = ["property_id", "title", "location",
    "property_type", "bedrooms", "bathrooms", "max_guests"]
    # another endpoint will handle searching by max and min price

    if (search_by is None) or (search_by not in search_range):
        raise HTTPException(
            status_code=400,
            detail="invalid search!"
        )
    if (search_input is None) or (not search_input):
        raise HTTPException(
            status_code=400,
            detail="invalid search!"
        )

    if search_by == "property_id":
        # check db for property id
        # raise 404 if not found, else return property info
        check_property_id = db.query(Property_Listings).filter(
        Property_Listings.listing_id == search_input).first()
        if check_property_id is None:
            raise HTTPException(
                status_code=404,
                detail="property does not exist!"
            )

        check_property = check_property_id.__dict__
        return {
            "statusCode": 200,
            "message": "success",
            "data": [check_property]
        }
    elif search_by == "max_guests":
        try:
            search_input = int(search_input)
        except:
            raise HTTPException(
                status_code=400,
                detail="invalid search!"
            )
        retrieve_max_guests = db.query(Property_Listings).filter(
        Property_Listings.max_guests == search_input
        ).order_by(Property_Listings.created_at.desc()
        ).limit(15).all()  # return 15 latest proerties that matches the max guests
        return {
            "statusCode": 200,
            "message": "success",
            "data": [
                {
                    column.name: getattr(row, column.name)
                    for column in Property_Listings.__table__.columns
                }
                for row in retrieve_max_guests
            ]
        }
    elif search_by == "bathrooms":
        try:
            search_input = int(search_input)
        except:
            raise HTTPException(
                status_code=400,
                detail="invalid search!"
            )
        retrieve_bathrooms = db.query(Property_Listings).filter(
        Property_Listings.bathrooms == search_input
        ).order_by(Property_Listings.created_at.desc()
        ).limit(15).all()  # return 15 latest proerties that matches the bathrooms
        return {
            "statusCode": 200,
            "message": "success",
            "data": [
                {
                    column.name: getattr(row, column.name)
                    for column in Property_Listings.__table__.columns
                }
                for row in retrieve_bathrooms
            ]
        }
    elif search_by == "bedrooms":
        try:
            search_input = int(search_input)
        except:
            raise HTTPException(
                status_code=400,
                detail="invalid search!"
            )
        retrieve_bedrooms = db.query(Property_Listings).filter(
        Property_Listings.bedrooms == search_input
        ).order_by(Property_Listings.created_at.desc()
        ).limit(15).all()  # return 15 latest properties that matches the bedrooms
        return {
            "statusCode": 200,
            "message": "success",
            "data": [
                {
                    column.name: getattr(row, column.name)
                    for column in Property_Listings.__table__.columns
                }
                for row in retrieve_bedrooms
            ]
        }
    elif search_by == "title":
        search_input = search_input.strip()
        
        if len(search_input) < 2:
            raise HTTPException(
                status_code=400,
                detail="search query too short!"
            )

        search_input_list = [
            i.strip()
            for i in search_input.split()
            if i.strip()
        ]

        match_score = sum(
            case(
                (Property_Listings.title.ilike(f"%{term}%"), 1),
                else_=0
            )
            for term in search_input_list
        )

        retrieve_title_search = (
            db.query(
                Property_Listings,
                match_score.label("score")
            ).filter(
            or_(
                *[
                    Property_Listings.title.ilike(f"%{term}%")
                    for term in search_input_list
                ]
            )).order_by(desc("score")).limit(15).all()
        )

        return {
            "statusCode": 200,
            "message": "success",
            "data": [
                {
                    **{
                        column.name: getattr(property_row, column.name)
                        for column in Property_Listings.__table__.columns
                    }
                }
                for property_row, score in retrieve_title_search
            ]
        }
    elif search_by == "location":
        search_input = search_input.strip()

        if len(search_input) < 1:
            raise HTTPException(
                status_code=400,
                detail="invalid search!"
            )

        search_input_list = [
            i.strip().lower()
            for i in search_input.split()
            if i.strip()
        ]

        if not search_input_list:
            raise HTTPException(
                status_code=400,
                detail="invalid search!"
            )

        query = db.query(Property_Listings)

        # STRICT MATCH: ALL terms must exist
        for term in search_input_list:
            query = query.filter(
                Property_Listings.location.ilike(f"%{term}%")
            )

        results = query.order_by(
            Property_Listings.created_at.desc()
        ).limit(15).all()

        return {
            "statusCode": 200,
            "message": "success",
            "data": [
                {
                    **{
                        column.name: getattr(row, column.name)
                        for column in Property_Listings.__table__.columns
                    }
                }
                for row in results
            ]
        }
    elif search_by == "property_type":
        search_input = search_input.strip()

        if len(search_input) < 1:
            raise HTTPException(
                status_code=400,
                detail="invalid search!"
            )

        results = (
            db.query(Property_Listings)
            .filter(
                Property_Listings.property_type.ilike(f"%{search_input}%")
            )
            .order_by(Property_Listings.created_at.desc())
            .limit(15)
            .all()
        )

        return {
            "statusCode": 200,
            "message": "success",
            "data": [
                {
                    **{
                        column.name: getattr(row, column.name)
                        for column in Property_Listings.__table__.columns
                    }
                }
                for row in results
            ]
        }
    else:
        return "not developed yet"
        
        
        
        
    

