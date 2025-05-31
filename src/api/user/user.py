from typing import List

import fastapi
from fastapi import APIRouter, Response, Depends, Query

from src.app.user.schemas import ExceptionResponseSchema, CreateUserResponseSchema, CreateUserRequestSchema, \
    GetUserListResponseSchema
from src.app.user.services.UserService import UserService
from src.utilities.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated

user_router = APIRouter()

class IsAdmin:
    pass


@user_router.get(
    "/list",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}}, dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)