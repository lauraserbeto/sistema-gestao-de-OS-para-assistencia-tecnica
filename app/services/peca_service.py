from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.peca import Peca
from app.repositories.peca_repository import PecaRepository
from app.schemas.peca import PecaCreate, PecaUpdate


class PecaService:
    def __init__(self, db: Session) -> None:
        self.repository = PecaRepository(db)

    def list(self, skip: int, limit: int) -> list[Peca]:
        return self.repository.list(skip=skip, limit=limit)

    def get(self, peca_id: int) -> Peca:
        peca = self.repository.get_by_id(peca_id)
        if not peca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Peca nao encontrada",
            )
        return peca

    def create(self, payload: PecaCreate) -> Peca:
        data = payload.model_dump()

        self._ensure_valid_stock(data["quantidade_estoque"])
        self._ensure_valid_price(data["valor_unitario"])

        return self.repository.create(Peca(**data))

    def update(self, peca_id: int, payload: PecaUpdate) -> Peca:
        peca = self.get(peca_id)
        data = payload.model_dump(exclude_unset=True)

        if "quantidade_estoque" in data:
            self._ensure_valid_stock(data["quantidade_estoque"])

        if "valor_unitario" in data:
            self._ensure_valid_price(data["valor_unitario"])

        return self.repository.update(peca, data)

    def delete(self, peca_id: int) -> None:
        peca = self.get(peca_id)
        self.repository.delete(peca)

    def _ensure_valid_stock(self, quantidade: int) -> None:
        if quantidade < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A quantidade em estoque nao pode ser negativa",
            )

    def _ensure_valid_price(self, valor) -> None:
        if valor < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O valor unitario nao pode ser negativo",
            )