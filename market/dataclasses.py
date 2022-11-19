from pydantic import Field

from core.services.dataclasses import SignFloat


class SignPrice(SignFloat):
    sign_value: str | None = Field(default=None, alias='price')
