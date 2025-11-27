from flask import Response
from app.config import settings


def set_cookie(response: Response, key: str, value: str, max_age: int):
    """
    Flask version of set_cookie.
    """
    response.set_cookie(
        key,
        value,
        httponly=True,
        samesite="None",
        secure=(settings.ENV == "prod"),
        max_age=max_age,
    )


def clear_cookie(response: Response, key: str):
    """
    Flask version of clear_cookie.
    """
    response.delete_cookie(
        key,
        samesite="None",
        secure=(settings.ENV == "prod"),
    )
