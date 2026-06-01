import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico


class UserRole(str, enum.Enum):
    administrador = "administrador"
    tecnico = "tecnico"
    atendente = "atendente"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda enum_: [item.value for item in enum_]),
        nullable=False,
        default=UserRole.atendente,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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

    ordens_como_tecnico: Mapped[list["OrdemServico"]] = relationship(
        "OrdemServico",
        back_populates="technician",
        foreign_keys="OrdemServico.technician_id",
    )
    ordens_abertas: Mapped[list["OrdemServico"]] = relationship(
        "OrdemServico",
        back_populates="opened_by",
        foreign_keys="OrdemServico.opened_by_id",
    )
