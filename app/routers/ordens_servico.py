from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.ordem_servico import OSPriority, OSStatus
from app.models.user import User, UserRole
from app.schemas.ordem_servico import OSAssign, OSCancel, OSCreate, OSResponse, OSUpdate
from app.services.os_service import OSService


router = APIRouter(prefix="/os", tags=["Ordens de Servico"])


@router.post(
    "",
    response_model=OSResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.administrador, UserRole.atendente))],
)
def create_os(
    payload: OSCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return OSService(db).create(payload, current_user)


@router.get(
    "",
    response_model=list[OSResponse],
    dependencies=[Depends(get_current_user)],
)
def list_os(
    status_filter: Optional[OSStatus] = Query(default=None, alias="status"),
    priority: Optional[OSPriority] = Query(default=None),
    client_id: Optional[int] = Query(default=None),
    technician_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Busca por titulo ou numero da OS"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return OSService(db).list(
        status_filter=status_filter,
        priority=priority,
        client_id=client_id,
        technician_id=technician_id,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{os_id}",
    response_model=OSResponse,
    dependencies=[Depends(get_current_user)],
)
def get_os(os_id: int, db: Session = Depends(get_db)):
    return OSService(db).get(os_id)


@router.put(
    "/{os_id}",
    response_model=OSResponse,
    dependencies=[Depends(require_roles(UserRole.administrador, UserRole.atendente))],
)
def update_os(os_id: int, payload: OSUpdate, db: Session = Depends(get_db)):
    return OSService(db).update(os_id, payload)


@router.patch(
    "/{os_id}/assign",
    response_model=OSResponse,
    dependencies=[Depends(require_roles(UserRole.administrador, UserRole.atendente))],
)
def assign_technician(os_id: int, payload: OSAssign, db: Session = Depends(get_db)):
    return OSService(db).assign_technician(os_id, payload)


@router.patch(
    "/{os_id}/close",
    response_model=OSResponse,
    dependencies=[Depends(require_roles(UserRole.administrador, UserRole.tecnico))],
)
def close_os(os_id: int, db: Session = Depends(get_db)):
    return OSService(db).close(os_id)


@router.patch(
    "/{os_id}/cancel",
    response_model=OSResponse,
    dependencies=[Depends(require_roles(UserRole.administrador, UserRole.atendente))],
)
def cancel_os(os_id: int, payload: OSCancel, db: Session = Depends(get_db)):
    return OSService(db).cancel(os_id, payload)
