import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.user import User


class OSStatus(str, enum.Enum):
    aberta = "aberta"
    em_andamento = "em_andamento"
    concluida = "concluida"
    cancelada = "cancelada"


class OSPriority(str, enum.Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    urgente = "urgente"


class OrdemServico(Base):
    __tablename__ = "ordens_servico"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    numero: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OSStatus] = mapped_column(
        Enum(OSStatus, values_callable=lambda e: [i.value for i in e]),
        nullable=False,
        default=OSStatus.aberta,
    )
    priority: Mapped[OSPriority] = mapped_column(
        Enum(OSPriority, values_callable=lambda e: [i.value for i in e]),
        nullable=False,
        default=OSPriority.media,
    )
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    technician_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    opened_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    assigned_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
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

    client: Mapped["Client"] = relationship("Client", back_populates="ordens_servico")
    technician: Mapped[Optional["User"]] = relationship(
        "User", back_populates="ordens_como_tecnico", foreign_keys=[technician_id]
    )
    opened_by: Mapped["User"] = relationship(
        "User", back_populates="ordens_abertas", foreign_keys=[opened_by_id]
    )
