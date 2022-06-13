# standard imports
import logging

# external imports
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# local imports
from api.api_v1.docs.openapi.api.routes.supported_langauges import (add_supported_language_response,
                                                                    fetch_all_languages_by_country_id_response)
from src import crud
from api import dependencies
from src.schemas import Paginate
from src.schemas.country_language import CountryLanguageCreate

logg = logging.getLogger()
router = APIRouter(prefix='/supportedLanguages')


@router.get("/{country_id}", responses=fetch_all_languages_by_country_id_response())
def fetch_all_languages_by_country_id(country_id: int, db: Session = Depends(dependencies.get_database)) -> JSONResponse:
    """Get all languages by country id
    :param db:
    :type db:
    :param country_id:
    :type country_id:
    :return:
    :rtype:
    """
    response = {}
    country = crud.country.get(db=db, object_id=country_id)
    if not country:
        response['message'] = 'Country not found.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
    languages = crud.supported_languages.get_country_supported_languages(db=db, country_id=country_id)
    response['message'] = "Supported languages successfully fetched."
    response['status'] = 0
    response['data'] = jsonable_encoder(languages)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@router.post("/add", responses=add_supported_language_response())
def add_supported_language(payload: CountryLanguageCreate, db: Session = Depends(dependencies.get_database)) -> JSONResponse:
    """Add a country
    :param db:
    :type db:
    :param payload: country to add
    """
    response = {}
    try:
        crud.supported_languages.create(db=db, obj_in=payload)
        response['message'] = 'Supported language successfully added.'
        response['status'] = 0
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except IntegrityError as error:
        logg.error(error)
        response['message'] = 'Country Language association already exists.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_409_CONFLICT)

