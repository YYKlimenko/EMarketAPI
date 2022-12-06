from datetime import datetime, timedelta
from typing import Any

import jwt
from bcrypt import checkpw
from fastapi import Body, HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.repositories import SQLAuthorizationRepository
from auth.configs import AuthConfig


class AuthorizationService:

    def __init__(self, repository=Depends(SQLAuthorizationRepository), config=Depends(AuthConfig)):
        self.repository = repository
        self.hash_key = config.SECRET_KEY
        self.user_model = config.USER_MODEL

    def encode_jwt(self, user_id: int, is_admin: bool):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=12),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'is_admin': is_admin
        }
        return jwt.encode(payload, self.hash_key, algorithm='HS256')

    async def authorize(
            self,
            login: str = Body(...),
            password: str = Body(...),
    ) -> dict[str, str]:
        user = await self.repository.get_auth_data('username', login, self.user_model)
        if user and checkpw(password.encode(), user['password'].encode()):
            return {
                "access_token": self.encode_jwt(user['id'], user['is_admin']),
                "token_type": "bearer"
            }
        else:
            raise HTTPException(401, detail='Not authorized')


class Authenticator:

    @staticmethod
    def decode_jwt(token: str, hash_key: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, hash_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    @staticmethod
    def handle_auth(
            auth: HTTPAuthorizationCredentials = Security(HTTPBearer()), config=Depends(AuthConfig)
    ) -> dict[str, Any]:
        return Authenticator.decode_jwt(auth.credentials, config.SECRET_KEY)
