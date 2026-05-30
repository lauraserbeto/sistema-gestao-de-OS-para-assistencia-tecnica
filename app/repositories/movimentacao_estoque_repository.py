from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movimentacao_estoque import MovimentacaoEstoque


class MovimentacaoEstoqueRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, movimentacao: MovimentacaoEstoque) -> MovimentacaoEstoque:
        self.db.add(movimentacao)
        self.db.commit()
        self.db.refresh(movimentacao)
        return movimentacao

    def listar(self, skip: int = 0, limit: int = 50) -> list[MovimentacaoEstoque]:
        statement = (
            select(MovimentacaoEstoque)
            .order_by(MovimentacaoEstoque.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def listar_por_peca(
        self,
        peca_id: int,
        skip: int = 0,
        limit: int = 50,
    ) -> list[MovimentacaoEstoque]:
        statement = (
            select(MovimentacaoEstoque)
            .where(MovimentacaoEstoque.peca_id == peca_id)
            .order_by(MovimentacaoEstoque.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())