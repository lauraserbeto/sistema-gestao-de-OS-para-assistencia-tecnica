from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ordem_servico import OrdemServico, OSStatus
from app.models.ordem_servico_peca import OrdemServicoPeca
from app.models.peca import Peca
from app.models.user import User


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def orders_by_status(self):
        return (
            self.db.query(
                OrdemServico.status,
                func.count(OrdemServico.id).label("total")
            )
            .group_by(OrdemServico.status)
            .all()
        )

    def late_orders(self):
        limite = datetime.now(timezone.utc) - timedelta(days=7)

        return (
            self.db.query(OrdemServico)
            .filter(
                OrdemServico.status != OSStatus.concluida,
                OrdemServico.created_at < limite
            )
            .all()
        )

    def top_technicians(self):
        return (
            self.db.query(
                User.name,
                func.count(OrdemServico.id).label("total")
            )
            .join(
                OrdemServico,
                OrdemServico.technician_id == User.id
            )
            .filter(
                OrdemServico.status == OSStatus.concluida
            )
            .group_by(User.id, User.name)
            .all()
        )

    def most_used_parts(self):
        return (
            self.db.query(
                Peca.nome,
                func.sum(
                    OrdemServicoPeca.quantidade
                ).label("total")
            )
            .join(
                OrdemServicoPeca,
                OrdemServicoPeca.peca_id == Peca.id
            )
            .group_by(Peca.id)
            .all()
        )

    def average_service_time(self):
        ordens = (
            self.db.query(OrdemServico)
            .filter(
                OrdemServico.status == OSStatus.concluida,
                OrdemServico.closed_at.isnot(None)
            )
            .all()
        )

        if not ordens:
            return 0

        total = 0

        for ordem in ordens:
            total += (
                ordem.closed_at - ordem.created_at
            ).total_seconds()

        return round(
            total / len(ordens) / 3600,
            2
        )