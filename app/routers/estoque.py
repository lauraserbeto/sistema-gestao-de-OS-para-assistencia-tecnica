from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import UserRole
from app.schemas.movimentacao_estoque import (
    MovimentacaoCreate,
    MovimentacaoEstoqueResponse,
)
from app.services.estoque_service import EstoqueService


router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"],
    #dependencies=[
        #Depends(require_roles(UserRole.administrador,  UserRole.tecnico)),
    #],
)


@router.post(
    "/entrada/{peca_id}",
    response_model=MovimentacaoEstoqueResponse,
)
def entrada_estoque(
    peca_id: int,
    payload: MovimentacaoCreate,
    db: Session = Depends(get_db),
):
    return EstoqueService(db).entrada(
        peca_id=peca_id,
        quantidade=payload.quantidade,
        observacao=payload.observacao,
    )


@router.post(
    "/saida/{peca_id}",
    response_model=MovimentacaoEstoqueResponse,
)
def saida_estoque(
    peca_id: int,
    payload: MovimentacaoCreate,
    db: Session = Depends(get_db),
):
    return EstoqueService(db).saida(
        peca_id=peca_id,
        quantidade=payload.quantidade,
        observacao=payload.observacao,
    )