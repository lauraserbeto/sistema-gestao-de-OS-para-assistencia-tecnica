from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.revoked_token import RevokedToken


class TokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def revoke(self, token: str, expires_at: datetime) -> RevokedToken:
        revoked = RevokedToken(token=token, expires_at=expires_at)
        self.db.add(revoked)
        self.db.commit()
        self.db.refresh(revoked)
        return revoked

    def is_revoked(self, token: str) -> bool:
        statement = select(RevokedToken.id).where(RevokedToken.token == token)
        return self.db.scalar(statement) is not None

    def remove_expired(self, now: datetime) -> None:
        self.db.execute(delete(RevokedToken).where(RevokedToken.expires_at <= now))
        self.db.commit()
