from fastapi import HTTPException, status
import httpx

from app.core.config import settings


class ViaCepService:
    def fetch_address(self, cep: str) -> dict[str, str]:
        url = f"{settings.viacep_base_url}/{cep}/json/"
        try:
            response = httpx.get(url, timeout=5)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Falha ao consultar ViaCEP",
            ) from exc

        data = response.json()
        if data.get("erro"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CEP nao encontrado no ViaCEP",
            )

        return {
            "street": data.get("logradouro") or "",
            "neighborhood": data.get("bairro") or "",
            "city": data.get("localidade") or "",
            "state": data.get("uf") or "",
        }
