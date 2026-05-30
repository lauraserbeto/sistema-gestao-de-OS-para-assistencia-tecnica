from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import UserRole
from app.schemas.peca import PecaCreate, PecaResponse, PecaUpdate
from app.services.peca_service import PecaService


router = APIRouter(
    prefix="/pecas",
    tags=["Peças"],
    #dependencies=[
        #Depends(require_roles(UserRole.administrador, #UserRole.tecnico)),
    #],
)


@router.post("", response_model=PecaResponse, status_code=status.HTTP_201_CREATED)
def create_peca(payload: PecaCreate, db: Session = Depends(get_db)):
    return PecaService(db).create(payload)


@router.get("", response_model=list[PecaResponse])
def list_pecas(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return PecaService(db).list(skip=skip, limit=limit)


@router.get("/{peca_id}", response_model=PecaResponse)
def get_peca(peca_id: int, db: Session = Depends(get_db)):
    return PecaService(db).get(peca_id)


@router.put("/{peca_id}", response_model=PecaResponse)
def update_peca(peca_id: int, payload: PecaUpdate, db: Session = Depends(get_db)):
    return PecaService(db).update(peca_id, payload)


@router.delete("/{peca_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_peca(peca_id: int, db: Session = Depends(get_db)):
    PecaService(db).delete(peca_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)