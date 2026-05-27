from app.core.security import get_password_hash
from app.database.session import SessionLocal
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository


def run() -> None:
    db = SessionLocal()
    try:
        repository = UserRepository(db)
        users = [
            ("Administrador", "admin@assistencia.com", "admin123", UserRole.administrador),
            ("Tecnico Padrao", "tecnico@assistencia.com", "tecnico123", UserRole.tecnico),
            ("Atendente Padrao", "atendente@assistencia.com", "atendente123", UserRole.atendente),
        ]
        for name, email, password, role in users:
            if repository.get_by_email(email):
                continue
            repository.create(
                User(
                    name=name,
                    email=email,
                    password_hash=get_password_hash(password),
                    role=role,
                )
            )
    finally:
        db.close()


if __name__ == "__main__":
    run()
