from typing import Optional, List

from sqlalchemy import select, and_, or_

from src.app.user.models.db_user import User
from src.app.user.schemas import LoginResponseSchema
from src.utilities.db import session, Transactional
from src.utilities.exceptions import UserNotFoundException, PasswordDoesNotMatchException, \
    DuplicateEmailOrNicknameException
from src.utilities.token_helper import TokenHelper
from passlib.context import CryptContext
from sqlalchemy import select, or_

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class UserService:
    def __init__(self):
        ...

    @Transactional()
    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(or_(User.email == email, User.nickname == nickname))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException
        hashed_password = hash_password(password1)
        user = User(email=email, password=hashed_password, nickname=nickname)
        session.add(user)

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(and_(User.email == email))
        )
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        if not verify_password(password, user.password):
            raise PasswordDoesNotMatchException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()