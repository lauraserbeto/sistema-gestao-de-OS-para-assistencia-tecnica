from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrdemServicoPecaCreate(BaseModel):
    peca_id: int
    quantidade: int = Field(..., gt=0)


class OrdemServicoPecaResponse(BaseModel):
    id: int
    ordem_servico_id: int
    peca_id: int
    quantidade: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)