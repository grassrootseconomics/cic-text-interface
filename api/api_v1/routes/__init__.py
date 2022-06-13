# standard imports

# external imports
from fastapi import APIRouter

# local imports
from . import country
from . import language
from . import supported_languages

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(country.router, tags=["country"])
api_router.include_router(language.router, tags=["language"])
api_router.include_router(supported_languages.router, tags=["supported_languages"])

