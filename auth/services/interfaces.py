from typing import Any


class AuthorizationRepository:

    async def get_auth_data(
            self, field: str, value: Any, session: Any, password_field: str = 'password'
    ) -> dict[str, str | int]:
        raise NotImplementedError
