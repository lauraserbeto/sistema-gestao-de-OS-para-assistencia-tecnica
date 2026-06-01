from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.ordem_servico import OSPriority, OSStatus, OrdemServico


class OSRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, os_id: int) -> Optional[OrdemServico]:
        return self.db.get(OrdemServico, os_id)

    def count_active_by_technician(
        self, technician_id: int, exclude_os_id: Optional[int] = None
    ) -> int:
        statement = (
            select(func.count())
            .select_from(OrdemServico)
            .where(
                OrdemServico.technician_id == technician_id,
                OrdemServico.status == OSStatus.em_andamento,
            )
        )
        if exclude_os_id is not None:
            statement = statement.where(OrdemServico.id != exclude_os_id)
        return self.db.scalar(statement) or 0

    def list(
        self,
        status: Optional[OSStatus] = None,
        priority: Optional[OSPriority] = None,
        client_id: Optional[int] = None,
        technician_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[OrdemServico]:
        statement = select(OrdemServico).order_by(OrdemServico.created_at.desc())
        if status is not None:
            statement = statement.where(OrdemServico.status == status)
        if priority is not None:
            statement = statement.where(OrdemServico.priority == priority)
        if client_id is not None:
            statement = statement.where(OrdemServico.client_id == client_id)
        if technician_id is not None:
            statement = statement.where(OrdemServico.technician_id == technician_id)
        if search:
            term = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    OrdemServico.title.ilike(term),
                    OrdemServico.numero.ilike(term),
                )
            )
        return list(self.db.scalars(statement.offset(skip).limit(limit)).all())

    def create(self, os: OrdemServico) -> OrdemServico:
        os.numero = self._next_numero()
        self.db.add(os)
        self.db.commit()
        self.db.refresh(os)
        return os

    def update(self, os: OrdemServico, data: dict) -> OrdemServico:
        for field, value in data.items():
            setattr(os, field, value)
        self.db.commit()
        self.db.refresh(os)
        return os

    def _next_numero(self) -> str:
        year = datetime.now().year
        count = self.db.scalar(select(func.count()).select_from(OrdemServico)) or 0
        return f"OS-{year}-{count + 1:06d}"
