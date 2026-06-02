from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Peca(Base):
    __tablename__ = "pecas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantidade_estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    valor_unitario: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )