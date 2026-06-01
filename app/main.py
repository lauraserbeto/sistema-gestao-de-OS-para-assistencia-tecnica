from fastapi import FastAPI

from app.core.config import settings
from app.routers import auth, clients, ordens_servico


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para gestao de ordens de servico de assistencia tecnica.",
)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(clients.router, prefix=settings.api_prefix)
app.include_router(ordens_servico.router, prefix=settings.api_prefix)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
