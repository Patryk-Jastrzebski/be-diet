import fastapi
from fastapi import APIRouter, Response, Depends

from src.api.auth.request.auth import RefreshTokenRequest, VerifyTokenRequest
from src.api.auth.response.auth import RefreshTokenResponse, LoginResponse
from src.app.auth.services.jwt import JwtService
from src.app.user.models.user import AccountInLogin
from src.app.user.schemas import ExceptionResponseSchema, CreateUserResponseSchema, CreateUserRequestSchema
from src.app.user.services.UserService import UserService
from src.utilities.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated

auth_router = APIRouter()

@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def refresh_token(request: RefreshTokenRequest):
    token = await JwtService().create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify")
async def verify_token(request: VerifyTokenRequest):
    await JwtService().verify_token(token=request.token)
    return Response(status_code=200)

@auth_router.post(
    "/login",
    response_model=LoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def login(request: AccountInLogin):
    token = await UserService().login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}

@auth_router.post(
    "/register",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema):
    await UserService().create_user(**request.dict())
    return {"email": request.email, "nickname": request.nickname}
