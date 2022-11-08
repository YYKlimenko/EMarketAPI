from datetime import datetime, timedelta
from typing import Any

import jwt
from bcrypt import checkpw
from fastapi import Body, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.services.interfaces import AuthorizationRepository
from auth.settings import DB_CONNECTOR


class AuthorizationService:

    def __init__(self, hash_key: str, repository: AuthorizationRepository):
        self._hash_key = hash_key
        self._repository = repository

    def encode_jwt(self, user_id: int):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=12),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self._hash_key, algorithm='HS256')

    async def authorize(
            self,
            login: str = Body(...),
            password: str = Body(...),
            session: AsyncSession = DB_CONNECTOR
    ) -> dict[str, str]:
        user = await self._repository.get_auth_data('username', login, session)
        if user and checkpw(password.encode(), user['password'].encode()):
            return {"access_token": self.encode_jwt(user['id']), "token_type": "bearer"}
        else:
            raise HTTPException(401, detail='Not authorized')


class Authenticator:
    def __init__(self, key: str) -> None:
        self._key = key

    def decode_jwt(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def handle_auth(
            self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> dict[str, Any]:
        return self.decode_jwt(auth.credentials)
