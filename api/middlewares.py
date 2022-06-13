# standard imports
from fastapi.middleware.cors import CORSMiddleware

# external imports
from fastapi import FastAPI

# local imports
from src.config import config


def handle_middlewares(app: FastAPI):
    # CORS middleware
    cors_origins = config.get("CORS_ORIGINS")

    origins = cors_origins.split(",") if cors_origins else ["*"]
    app.add_middleware(CORSMiddleware,
                       allow_origins=origins,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])
