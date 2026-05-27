from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.viacep_service import ViaCepService


class ClientService:
    def __init__(self, db: Session) -> None:
        self.repository = ClientRepository(db)
        self.viacep = ViaCepService()

    def list(self, search: str | None, skip: int, limit: int) -> list[Client]:
        return self.repository.list(search=search, skip=skip, limit=limit)

    def get(self, client_id: int) -> Client:
        client = self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente nao encontrado",
            )
        return client

    def create(self, payload: ClientCreate) -> Client:
        data = payload.model_dump()
        self._ensure_unique(cpf=data["cpf"], email=data["email"])
        data = self._complete_address(data)
        self._ensure_required_address(data)
        return self.repository.create(Client(**data))

    def update(self, client_id: int, payload: ClientUpdate) -> Client:
        client = self.get(client_id)
        data = payload.model_dump(exclude_unset=True)

        cpf = data.get("cpf")
        if cpf and cpf != client.cpf and self.repository.get_by_cpf(cpf):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF ja cadastrado")

        email = data.get("email")
        if email and email != client.email and self.repository.get_by_email(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail ja cadastrado")

        if "cep" in data:
            data = self._complete_address(data)

        merged = {
            "street": data.get("street", client.street),
            "neighborhood": data.get("neighborhood", client.neighborhood),
            "city": data.get("city", client.city),
            "state": data.get("state", client.state),
        }
        self._ensure_required_address(merged)
        return self.repository.update(client, data)

    def delete(self, client_id: int) -> None:
        client = self.get(client_id)
        self.repository.delete(client)

    def _ensure_unique(self, cpf: str, email: str) -> None:
        if self.repository.get_by_cpf(cpf):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF ja cadastrado")
        if self.repository.get_by_email(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail ja cadastrado")

    def _complete_address(self, data: dict) -> dict:
        cep = data.get("cep")
        if not cep:
            return data

        via_cep_data = self.viacep.fetch_address(cep)
        for field, value in via_cep_data.items():
            if not data.get(field):
                data[field] = value
        return data

    def _ensure_required_address(self, data: dict) -> None:
        missing = [
            field
            for field in ("street", "neighborhood", "city", "state")
            if not data.get(field)
        ]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Endereco incompleto. Campos ausentes: {', '.join(missing)}",
            )
