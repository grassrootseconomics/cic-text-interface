# standard imports

# external imports
from fastapi import FastAPI

# local imports
from api.api_v1 import routes


def handle_routes(app: FastAPI):
    app.include_router(router=routes.api_router)
