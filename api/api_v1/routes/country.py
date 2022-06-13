# standard imports
import logging

# external imports
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# local imports
from api import dependencies
from api.api_v1.docs.openapi.api.routes.country import (add_country_endpoint_responses,
                                                        fetch_all_countries_endpoint_responses,
                                                        update_country_endpoint_responses)
from src.config import config
from src import crud
from src.schemas import Paginate
from src.schemas.country import CountryCreate, CountryUpdate
from tasks import sync_supported_languages


logg = logging.getLogger()
router = APIRouter(prefix='/countries')


@router.get("", responses=fetch_all_countries_endpoint_responses())
def fetch_all_countries(db: Session = Depends(dependencies.get_database),
                        limit: int = Query(
                            default=100,
                            title="limit",
                            description="the row to end at when filtering query results (pagination end)",
                        ),
                        skip: int = Query(
                            default=0,
                            title="skip",
                            description="the row to start from when filtering query results (pagination start)")
                        ) -> Paginate:
    """This function fetches all countries from the database.
    :param db: A database session object.
    :type db: Session
    :param limit: The number of rows to return.
    :type limit: int
    :param skip: The number of rows to skip.
    :type skip: int
    :return: A Paginate object.
    :rtype: Paginate
    """
    countries = crud.country.get_multi(db=db, limit=limit, skip=skip)
    return Paginate(values=countries, total=len(countries), prev_link="", next_link="")


@router.post("/add", responses=add_country_endpoint_responses())
def add_country(payload: CountryCreate, db: Session = Depends(dependencies.get_database)) -> JSONResponse:
    """This endpoint adds a country object to the database.
    :param db: A database session object.
    :type db: Session
    :param payload: Country object to be added to the database.
    :type payload: CountryCreate
    :return: A JSON response containing the country object that was added to the database.
    :rtype: JSONResponse
    """
    response = {}
    try:
        country = crud.country.create(db=db, obj_in=payload)
        response['message'] = 'Country successfully added.'
        response['status'] = 0
        response['data'] = jsonable_encoder(country)
        sync_supported_languages.apply_async(queue=config.get("WORKER_QUEUE"))
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except IntegrityError as error:
        logg.error(error)
        response['message'] = 'Country already exists.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_409_CONFLICT)


@router.patch("/update/{country_id}", responses=update_country_endpoint_responses())
def update_country(payload: CountryUpdate,
                   country_id: int,
                   db: Session = Depends(dependencies.get_database)) -> JSONResponse:
    """This endpoint updates a country object in the database.
    :param db: A database session object.
    :type db: Session
    :param payload: Country data to update.
    :type payload: CountryUpdate
    :param country_id: id of the country object to update.
    :type country_id: int
    :return: A JSON response containing the country object that was updated in the database.
    :rtype: JSONResponse
    """
    response = {}
    country = crud.country.get(db=db, object_id=country_id)
    if not country:
        response['message'] = 'Country not found.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
    try:
        updated_country = crud.country.update(db=db, db_obj=country, obj_in=payload)
        response['message'] = 'Country successfully updated.'
        response['status'] = 0
        response['data'] = jsonable_encoder(updated_country)
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as error:
        logg.error(error)
        response['message'] = 'Country not updated.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
