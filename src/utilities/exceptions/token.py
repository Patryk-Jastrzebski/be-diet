from http import HTTPStatus

from src.utilities.exceptions.base import CustomException


class DecodeTokenException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = "Token expired"