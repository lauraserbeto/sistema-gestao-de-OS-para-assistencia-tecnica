from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.movimentacao_estoque_repository import (
    MovimentacaoEstoqueRepository,
)
from app.schemas.movimentacao_estoque import MovimentacaoEstoqueResponse


router = APIRouter(
    prefix="/movimentacoes-estoque",
    tags=["Movimentações de Estoque"],
)


@router.get("", response_model=list[MovimentacaoEstoqueResponse])
def listar_movimentacoes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return MovimentacaoEstoqueRepository(db).listar(skip=skip, limit=limit)


@router.get("/peca/{peca_id}", response_model=list[MovimentacaoEstoqueResponse])
def listar_movimentacoes_por_peca(
    peca_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return MovimentacaoEstoqueRepository(db).listar_por_peca(
        peca_id=peca_id,
        skip=skip,
        limit=limit,
    )