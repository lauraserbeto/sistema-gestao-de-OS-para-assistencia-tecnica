from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico
    from app.models.peca import Peca


class OrdemServicoPeca(Base):
    __tablename__ = "ordem_servico_pecas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ordem_servico_id: Mapped[int] = mapped_column(
        ForeignKey("ordens_servico.id"),
        nullable=False,
        index=True,
    )
    peca_id: Mapped[int] = mapped_column(
        ForeignKey("pecas.id"),
        nullable=False,
        index=True,
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    ordem_servico: Mapped["OrdemServico"] = relationship("OrdemServico")
    peca: Mapped["Peca"] = relationship("Peca")