from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.peca import Peca


class PecaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, peca_id: int) -> Peca | None:
        return self.db.get(Peca, peca_id)

    def list(self, skip: int = 0, limit: int = 50) -> list[Peca]:
        statement = (
            select(Peca)
            .order_by(Peca.nome)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def create(self, peca: Peca) -> Peca:
        self.db.add(peca)
        self.db.commit()
        self.db.refresh(peca)
        return peca

    def update(self, peca: Peca, data: dict) -> Peca:
        for field, value in data.items():
            setattr(peca, field, value)

        self.db.commit()
        self.db.refresh(peca)
        return peca

    def delete(self, peca: Peca) -> None:
        self.db.delete(peca)
        self.db.commit()