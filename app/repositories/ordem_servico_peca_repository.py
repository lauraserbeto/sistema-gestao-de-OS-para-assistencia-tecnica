from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ordem_servico_peca import OrdemServicoPeca


class OrdemServicoPecaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, item: OrdemServicoPeca) -> OrdemServicoPeca:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_by_os(self, ordem_servico_id: int) -> list[OrdemServicoPeca]:
        statement = (
            select(OrdemServicoPeca)
            .where(OrdemServicoPeca.ordem_servico_id == ordem_servico_id)
            .order_by(OrdemServicoPeca.created_at.desc())
        )
        return list(self.db.scalars(statement).all())