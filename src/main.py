import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing_extensions import List

from src.api.endpoints import router as api_endpoint_router
from src.config.manager import settings
from src.utilities.exceptions import CustomException
from src.utilities.exceptions.ExceptionHandler import ExceptionHandler
from src.utilities.middlewares.authentication import AuthenticationMiddleware, AuthBackend
from src.utilities.middlewares.sqlalchemy import SQLAlchemyMiddleware


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware)
    ]
    return middleware


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes, middleware=make_middleware())  # type: ignore

    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.ALLOWED_ORIGINS,
    #     allow_methods=settings.ALLOWED_METHODS,
    #     allow_headers=settings.ALLOWED_HEADERS,
    # )
    #
    # app.add_middleware(
    #     AuthenticationMiddleware,
    #     backend=AuthBackend()
    # )

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)
    ExceptionHandler.init_listeners(app_=app)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )