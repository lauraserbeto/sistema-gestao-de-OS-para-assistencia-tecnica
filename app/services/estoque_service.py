from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.repositories.movimentacao_estoque_repository import (
    MovimentacaoEstoqueRepository,
)
from app.repositories.peca_repository import PecaRepository


class EstoqueService:
    def __init__(self, db: Session) -> None:
        self.peca_repository = PecaRepository(db)
        self.movimentacao_repository = MovimentacaoEstoqueRepository(db)

    def entrada(
        self,
        peca_id: int,
        quantidade: int,
        observacao: str | None = None,
    ) -> MovimentacaoEstoque:
        peca = self.peca_repository.get_by_id(peca_id)

        if not peca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Peca nao encontrada",
            )

        estoque_anterior = peca.quantidade_estoque
        estoque_atual = estoque_anterior + quantidade

        self.peca_repository.update(
            peca,
            {"quantidade_estoque": estoque_atual},
        )

        movimentacao = MovimentacaoEstoque(
            peca_id=peca.id,
            tipo="ENTRADA",
            quantidade=quantidade,
            estoque_anterior=estoque_anterior,
            estoque_atual=estoque_atual,
            observacao=observacao,
        )

        return self.movimentacao_repository.create(movimentacao)

    def saida(
        self,
        peca_id: int,
        quantidade: int,
        observacao: str | None = None,
    ) -> MovimentacaoEstoque:
        peca = self.peca_repository.get_by_id(peca_id)

        if not peca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Peca nao encontrada",
            )

        if peca.quantidade_estoque < quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estoque insuficiente",
            )

        estoque_anterior = peca.quantidade_estoque
        estoque_atual = estoque_anterior - quantidade

        self.peca_repository.update(
            peca,
            {"quantidade_estoque": estoque_atual},
        )

        movimentacao = MovimentacaoEstoque(
            peca_id=peca.id,
            tipo="SAIDA",
            quantidade=quantidade,
            estoque_anterior=estoque_anterior,
            estoque_atual=estoque_atual,
            observacao=observacao,
        )

        return self.movimentacao_repository.create(movimentacao)