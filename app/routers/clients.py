from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import UserRole
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.services.client_service import ClientService


router = APIRouter(
    prefix="/clients",
    tags=["Clientes"],
    dependencies=[
        Depends(require_roles(UserRole.administrador, UserRole.atendente)),
    ],
)


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    return ClientService(db).create(payload)


@router.get("", response_model=list[ClientResponse])
def list_clients(
    search: str | None = Query(default=None, description="Busca por nome, CPF, email ou telefone"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return ClientService(db).list(search=search, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return ClientService(db).get(client_id)


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    return ClientService(db).update(client_id, payload)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    ClientService(db).delete(client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
