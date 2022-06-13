# standard imports

# external imports
from fastapi import FastAPI

# local imports
from api.middlewares import handle_middlewares
from api.api_v1.routing import handle_routes
from src.cache import initialize_cache
from src.config import config
from src.worker.celery_utils import create_celery_app
from version import __version__


def create_app() -> FastAPI:
    server = FastAPI(
        debug=True,
        title="CIC text interface server",
        description="",
        version=__version__,
        terms_of_service="",
        openapi_url="/openapi.json",
        license_info={
            "name": "GPL3",
        }
    )
    server.celery_app = create_celery_app(config)
    return server


app = create_app()
handle_middlewares(app)
handle_routes(app)
initialize_cache(config)
celery = app.celery_app


@app.get("/version", response_model=str)
def version():
    return __version__
