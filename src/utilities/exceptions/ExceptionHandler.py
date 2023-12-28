from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.utilities.exceptions import CustomException


class ExceptionHandler:
    @staticmethod
    def init_listeners(app_: FastAPI) -> None:
        # Exception handler
        @app_.exception_handler(CustomException)
        async def custom_exception_handler(request: Request, exc: CustomException):
            return JSONResponse(
                status_code=exc.code,
                content={"httpCode": exc.error_code, "message": exc.message},
            )