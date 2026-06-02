from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ordem_servico import OSPriority, OSStatus, OrdemServico
from app.models.user import User, UserRole
from app.repositories.client_repository import ClientRepository
from app.repositories.os_repository import OSRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ordem_servico import OSAssign, OSCancel, OSCreate, OSUpdate

from app.models.ordem_servico_peca import OrdemServicoPeca
from app.repositories.ordem_servico_peca_repository import OrdemServicoPecaRepository
from app.repositories.peca_repository import PecaRepository
from app.schemas.ordem_servico_peca import OrdemServicoPecaCreate
from app.services.estoque_service import EstoqueService

_MAX_ACTIVE_PER_TECH = 5
_TERMINAL = {OSStatus.concluida, OSStatus.cancelada}


class OSService:
    def __init__(self, db: Session) -> None:
        self.repo = OSRepository(db)
        self.client_repo = ClientRepository(db)
        self.user_repo = UserRepository(db)
        self.peca_repo = PecaRepository(db)
        self.os_peca_repo = OrdemServicoPecaRepository(db)
        self.estoque_service = EstoqueService(db)

    # ------------------------------------------------------------------ queries

    def get(self, os_id: int) -> OrdemServico:
        os = self.repo.get_by_id(os_id)
        if not os:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ordem de servico nao encontrada",
            )
        return os

    def list(
        self,
        status_filter: Optional[OSStatus] = None,
        priority: Optional[OSPriority] = None,
        client_id: Optional[int] = None,
        technician_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[OrdemServico]:
        return self.repo.list(
            status=status_filter,
            priority=priority,
            client_id=client_id,
            technician_id=technician_id,
            search=search,
            skip=skip,
            limit=limit,
        )

    # ------------------------------------------------------------------ mutations

    def create(self, payload: OSCreate, current_user: User) -> OrdemServico:
        if not self.client_repo.get_by_id(payload.client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente nao encontrado",
            )

        os_status = OSStatus.aberta
        assigned_at: Optional[datetime] = None

        if payload.technician_id is not None:
            self._validate_tech(payload.technician_id)
            self._check_tech_capacity(payload.technician_id)
            os_status = OSStatus.em_andamento
            assigned_at = datetime.now(timezone.utc)

        os = OrdemServico(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=os_status,
            client_id=payload.client_id,
            technician_id=payload.technician_id,
            opened_by_id=current_user.id,
            assigned_at=assigned_at,
        )
        return self.repo.create(os)

    def update(self, os_id: int, payload: OSUpdate) -> OrdemServico:
        os = self.get(os_id)
        self._guard_terminal(os)

        data = payload.model_dump(exclude_unset=True)
        if "client_id" in data and not self.client_repo.get_by_id(data["client_id"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente nao encontrado",
            )
        return self.repo.update(os, data)

    def assign_technician(self, os_id: int, payload: OSAssign) -> OrdemServico:
        os = self.get(os_id)
        self._guard_terminal(os)
        self._validate_tech(payload.technician_id)
        # exclude_os_id evita dupla contagem quando é o mesmo técnico sendo reatribuído
        self._check_tech_capacity(payload.technician_id, exclude_os_id=os_id)

        data: dict = {
            "technician_id": payload.technician_id,
            "assigned_at": datetime.now(timezone.utc),
        }
        if os.status == OSStatus.aberta:
            data["status"] = OSStatus.em_andamento
        return self.repo.update(os, data)

    def close(self, os_id: int) -> OrdemServico:
        os = self.get(os_id)
        if os.status != OSStatus.em_andamento:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Apenas ordens em andamento podem ser concluidas",
            )
        # Regra: não pode concluir sem técnico responsável
        if os.technician_id is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nao e possivel concluir uma OS sem tecnico responsavel",
            )
        return self.repo.update(os, {
            "status": OSStatus.concluida,
            "closed_at": datetime.now(timezone.utc),
        })

    def cancel(self, os_id: int, payload: OSCancel) -> OrdemServico:
        os = self.get(os_id)
        if os.status in _TERMINAL:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nao e possivel cancelar uma OS ja concluida ou cancelada",
            )
        return self.repo.update(os, {
            "status": OSStatus.cancelada,
            "cancellation_reason": payload.cancellation_reason,
        })
    
    def adicionar_peca(self, os_id: int, payload: OrdemServicoPecaCreate) -> OrdemServicoPeca:
        os = self.get(os_id)
        self._guard_terminal(os)

        peca = self.peca_repo.get_by_id(payload.peca_id)
        if not peca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Peca nao encontrada",
            )

        if peca.quantidade_estoque < payload.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estoque insuficiente",
            )

        self.estoque_service.saida(
            peca_id=payload.peca_id,
            quantidade=payload.quantidade,
            observacao=f"Utilizacao na OS {os.numero}",
        )

        item = OrdemServicoPeca(
            ordem_servico_id=os.id,
            peca_id=payload.peca_id,
            quantidade=payload.quantidade,
        )

        return self.os_peca_repo.create(item)

    # ------------------------------------------------------------------ helpers

    def _validate_tech(self, technician_id: int) -> User:
        tech = self.user_repo.get_by_id(technician_id)
        if not tech:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tecnico nao encontrado",
            )
        if tech.role != UserRole.tecnico:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O usuario indicado nao possui perfil de tecnico",
            )
        if not tech.is_active:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Tecnico inativo",
            )
        return tech

    def _check_tech_capacity(
        self, technician_id: int, exclude_os_id: Optional[int] = None
    ) -> None:
        count = self.repo.count_active_by_technician(technician_id, exclude_os_id=exclude_os_id)
        if count >= _MAX_ACTIVE_PER_TECH:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tecnico ja possui {_MAX_ACTIVE_PER_TECH} ordens em andamento (limite maximo)",
            )

    def _guard_terminal(self, os: OrdemServico) -> None:
        if os.status in _TERMINAL:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nao e possivel editar uma OS concluida ou cancelada",
            )
