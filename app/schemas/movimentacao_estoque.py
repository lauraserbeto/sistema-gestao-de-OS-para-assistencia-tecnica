from datetime import datetime

from pydantic import BaseModel, ConfigDict

from pydantic import BaseModel, Field


class MovimentacaoEstoqueResponse(BaseModel):
    id: int
    peca_id: int
    tipo: str
    quantidade: int
    estoque_anterior: int
    estoque_atual: int
    observacao: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovimentacaoCreate(BaseModel):
    quantidade: int = Field(..., gt=0)
    observacao: str | None = None