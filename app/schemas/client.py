from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


def only_digits(value: str | None) -> str | None:
    if value is None:
        return None
    return re.sub(r"\D", "", value)


class ClientBase(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    cpf: str = Field(min_length=11, max_length=14)
    phone: str = Field(min_length=8, max_length=20)
    email: str = Field(max_length=180)
    cep: str | None = Field(default=None, min_length=8, max_length=9)
    street: str | None = Field(default=None, max_length=180)
    number: str = Field(min_length=1, max_length=20)
    complement: str | None = Field(default=None, max_length=120)
    neighborhood: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    state: str | None = Field(default=None, min_length=2, max_length=2)

    @field_validator("cpf")
    @classmethod
    def normalize_cpf(cls, value: str) -> str:
        digits = only_digits(value) or ""
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 digitos")
        return digits

    @field_validator("cep")
    @classmethod
    def normalize_cep(cls, value: str | None) -> str | None:
        digits = only_digits(value)
        if digits is not None and len(digits) != 8:
            raise ValueError("CEP deve conter 8 digitos")
        return digits

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or "." not in normalized.split("@")[-1]:
            raise ValueError("email invalido")
        return normalized

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        digits = only_digits(value) or ""
        if len(digits) < 8:
            raise ValueError("telefone invalido")
        return digits

    @field_validator("state")
    @classmethod
    def normalize_state(cls, value: str | None) -> str | None:
        return value.upper() if value else value


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=120)
    cpf: str | None = Field(default=None, min_length=11, max_length=14)
    phone: str | None = Field(default=None, min_length=8, max_length=20)
    email: str | None = Field(default=None, max_length=180)
    cep: str | None = Field(default=None, min_length=8, max_length=9)
    street: str | None = Field(default=None, max_length=180)
    number: str | None = Field(default=None, min_length=1, max_length=20)
    complement: str | None = Field(default=None, max_length=120)
    neighborhood: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    state: str | None = Field(default=None, min_length=2, max_length=2)

    _normalize_cpf = field_validator("cpf")(ClientBase.normalize_cpf.__func__)
    _normalize_cep = field_validator("cep")(ClientBase.normalize_cep.__func__)
    _normalize_email = field_validator("email")(ClientBase.validate_email.__func__)
    _normalize_phone = field_validator("phone")(ClientBase.normalize_phone.__func__)
    _normalize_state = field_validator("state")(ClientBase.normalize_state.__func__)


class ClientResponse(BaseModel):
    id: int
    name: str
    cpf: str
    phone: str
    email: str
    cep: str | None
    street: str
    number: str
    complement: str | None
    neighborhood: str
    city: str
    state: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
