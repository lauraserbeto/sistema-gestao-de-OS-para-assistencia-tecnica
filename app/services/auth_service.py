from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)
        self.token_repository = TokenRepository(db)

    def register(self, payload: UserCreate) -> User:
        if self.repository.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail ja cadastrado",
            )

        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
            role=payload.role,
        )
        return self.repository.create(user)

    def authenticate(self, email: str, password: str) -> TokenResponse:
        user = self.repository.get_by_email(email.strip().lower())
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais invalidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inativo",
            )

        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token, user=user)

    def logout(self, token: str) -> None:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        self.token_repository.remove_expired(datetime.now(timezone.utc))
        if not self.token_repository.is_revoked(token):
            self.token_repository.revoke(token, expires_at)
