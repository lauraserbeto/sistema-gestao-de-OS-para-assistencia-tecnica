from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PecaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    descricao: str | None = None
    quantidade_estoque: int = Field(default=0, ge=0)
    valor_unitario: Decimal = Field(default=0, ge=0)


class PecaCreate(PecaBase):
    pass


class PecaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=120)
    descricao: str | None = None
    quantidade_estoque: int | None = Field(default=None, ge=0)
    valor_unitario: Decimal | None = Field(default=None, ge=0)


class PecaResponse(PecaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)