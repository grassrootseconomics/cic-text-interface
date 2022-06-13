# standard imports
import logging

# external imports
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# local imports
from api.api_v1.docs.openapi.api.routes.language import (add_language_endpoint_responses,
                                                         fetch_all_languages_endpoint_responses,
                                                         update_language_endpoint_responses)
from src import crud
from api import dependencies
from src.schemas import Paginate
from src.schemas.language import LanguageCreate, LanguageUpdate

logg = logging.getLogger()
router = APIRouter(prefix='/languages')


@router.get("", responses=fetch_all_languages_endpoint_responses())
def fetch_all_languages(db: Session = Depends(dependencies.get_database),
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
    """Get all languages
    :param db:
    :type db:
    :param limit:
    :type limit:
    :param skip:
    :type skip:
    :return:
    :rtype:
    """
    languages = crud.language.get_multi(db=db, limit=limit, skip=skip)
    return Paginate(values=languages, total=len(languages), prev_link="", next_link="")


@router.post("/add", responses=add_language_endpoint_responses())
def add_language(payload: LanguageCreate, db: Session = Depends(dependencies.get_database)) -> JSONResponse:
    """Add a language
    :param db:
    :type db:
    :param payload: language to add
    """
    response = {}
    try:
        language = crud.language.create(db=db, obj_in=payload)
        response['message'] = 'Language successfully added.'
        response['status'] = 0
        response['data'] = jsonable_encoder(language)
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except IntegrityError as error:
        logg.error(error)
        response['message'] = 'Language already exists.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_409_CONFLICT)


@router.patch("/update/{language_id}", responses=update_language_endpoint_responses())
def update_language(payload: LanguageUpdate,
                    language_id: int,
                    db: Session = Depends(dependencies.get_database)) -> JSONResponse:
    """
    """
    response = {}
    language = crud.language.get(db=db, object_id=language_id)
    if not language:
        response['message'] = 'Language not found.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
    try:
        updated_language = crud.language.update(db=db, db_obj=language, obj_in=payload)
        response['message'] = 'Language successfully updated.'
        response['status'] = 0
        response['data'] = jsonable_encoder(updated_language)
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as error:
        logg.error(error)
        response['message'] = 'Language not updated.'
        response['status'] = 1
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
