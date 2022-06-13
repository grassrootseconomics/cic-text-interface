# standard imports

# external imports
from fastapi import status

# local imports
from src.schemas import ApiResponse
from src.schemas.language import LanguageApiResponse
from src.schemas.utils import Paginate


def fetch_all_languages_endpoint_responses():
    return {
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "next_link": "",
                        "prev_link": "",
                        "total": 3,
                        "values": [
                            {
                                "id": 1,
                                "name": "English",
                                "symbol": "en"
                            },
                        ]
                    }
                }
            },
            "description": "Successful response.",
            "model": Paginate
        },
    }


def add_language_endpoint_responses():
    return {
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "name": "English",
                            "symbol": "en"
                        },
                        "message": "Language successfully added.",
                        "status": 0,
                    }
                }
            },
            "description": "Successful response.",
            "model": LanguageApiResponse
        },
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Language already exists.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        }
    }


def update_language_endpoint_responses():
    return {
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "code": "ke",
                            "name": "Kenya"
                        },
                        "message": "Language successfully updated.",
                        "status": 0
                    }
                }
            },
            "description": "Successful response.",
            "model": LanguageApiResponse
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Language not found.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Language not updated.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        }
    }
