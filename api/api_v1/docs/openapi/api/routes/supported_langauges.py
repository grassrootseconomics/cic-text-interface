# external imports
from fastapi import status

# local imports
from src.schemas import ApiResponse
from src.schemas.country_language import CountryLanguageApiResponse


def fetch_all_languages_by_country_id_response():
    return {
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": 1,
                                "name": "English",
                                "symbol": "en"
                            },
                        ],
                        "message": "Supported languages successfully fetched.",
                        "status": 0
                    }
                }
            },
            "description": "Successful response.",
            "model": CountryLanguageApiResponse
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Country not found.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        }
    }


def add_supported_language_response():
    return {
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Supported language successfully added.",
                        "status": 0,
                    }
                }
            },
            "description": "Successful response.",
            "model": ApiResponse
        },
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Country Language association already exists.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        }
    }