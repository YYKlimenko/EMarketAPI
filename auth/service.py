from datetime import datetime, timedelta
from typing import Any

import jwt
from bcrypt import checkpw
from fastapi import Body, HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.repositories import SQLAuthorizationRepository
from auth.settings import SECRET_KEY


class AuthorizationService:
    hash_key = SECRET_KEY

    def __init__(self, repository=Depends(SQLAuthorizationRepository)):
        self.repository = repository

    def encode_jwt(self, user_id: int):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=12),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.hash_key, algorithm='HS256')

    async def authorize(
            self,
            login: str = Body(...),
            password: str = Body(...),
    ) -> dict[str, str]:
        user = await self.repository.get_auth_data('username', login)
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
