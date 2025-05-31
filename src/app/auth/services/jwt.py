from datetime import timedelta, datetime

from src.app.auth.schemas.jwt import RefreshTokenSchema
from src.utilities.exceptions.token import DecodeTokenException
from src.utilities.token_helper import TokenHelper
import jwt

class JwtService:
    async def verify_token(self, token: str) -> None:
        TokenHelper.decode(token=token)

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenSchema:
        token = TokenHelper.decode(token=token)
        refresh_token = TokenHelper.decode(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenSchema(
            token=TokenHelper.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
    async def create_access_token(user_data: dict, expiry: timedelta):
        payload = { }

        payload['user'] = user_data
        payload['exp'] = not datetime.now() + expiry

        token = TokenHelper.encode()