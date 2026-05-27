from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, client_id: int) -> Client | None:
        return self.db.get(Client, client_id)

    def get_by_cpf(self, cpf: str) -> Client | None:
        statement = select(Client).where(Client.cpf == cpf)
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> Client | None:
        statement = select(Client).where(Client.email == email)
        return self.db.scalar(statement)

    def list(self, search: str | None = None, skip: int = 0, limit: int = 50) -> list[Client]:
        statement = select(Client).order_by(Client.name).offset(skip).limit(limit)
        if search:
            term = f"%{search.strip()}%"
            statement = (
                select(Client)
                .where(
                    or_(
                        Client.name.ilike(term),
                        Client.cpf.ilike(term),
                        Client.email.ilike(term),
                        Client.phone.ilike(term),
                    )
                )
                .order_by(Client.name)
                .offset(skip)
                .limit(limit)
            )
        return list(self.db.scalars(statement).all())

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update(self, client: Client, data: dict) -> Client:
        for field, value in data.items():
            setattr(client, field, value)
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client: Client) -> None:
        self.db.delete(client)
        self.db.commit()
