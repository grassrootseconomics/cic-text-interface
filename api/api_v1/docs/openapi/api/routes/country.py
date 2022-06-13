# standard imports

# external imports
from fastapi import status

# local imports
from src.schemas import ApiResponse
from src.schemas.country import CountryApiResponse
from src.schemas.utils import Paginate


def fetch_all_countries_endpoint_responses():
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
                                "code": "ke",
                                "id": 1,
                                "name": "Kenya"
                            },
                        ]
                    }
                }
            },
            "description": "Successful response.",
            "model": Paginate
        },
    }


def add_country_endpoint_responses():
    return {
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "code": "ke",
                            "name": "Kenya"
                        },
                        "message": "Country successfully added.",
                        "status": 0,
                    }
                }
            },
            "description": "Successful response.",
            "model": CountryApiResponse
        },
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Country already exists.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        }
    }


def update_country_endpoint_responses():
    return {
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "code": "ke",
                            "name": "Kenya"
                        },
                        "message": "Country successfully updated.",
                        "status": 0
                    }
                }
            },
            "description": "Successful response.",
            "model": CountryApiResponse
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
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Country not updated.",
                        "status": 1
                    }
                }
            },
            "description": "Failed response.",
            "model": ApiResponse
        }
    }
