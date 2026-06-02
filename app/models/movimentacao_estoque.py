from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    peca_id: Mapped[int] = mapped_column(ForeignKey("pecas.id"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    estoque_anterior: Mapped[int] = mapped_column(Integer, nullable=False)
    estoque_atual: Mapped[int] = mapped_column(Integer, nullable=False)
    observacao: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    peca = relationship("Peca")