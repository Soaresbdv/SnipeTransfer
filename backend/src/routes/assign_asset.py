import os
import csv
from typing import List, Optional
from fastapi import HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel

CSV_PATH = os.path.join("storage", "transferencias.csv")
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

class AssetInput(BaseModel):
    username: str
    asset_tag: str
    flag: Optional[str] = None  # opcional; não será exportado

def _format_asset_tag(value: str) -> str:
    digits = "".join(ch for ch in value.upper().replace("ST", "") if ch.isdigit())
    if not digits:
        raise HTTPException(status_code=400, detail="asset_tag inválido")
    if len(digits) > 4:
        raise HTTPException(status_code=400, detail="asset_tag deve ter no máximo 4 dígitos")
    return "ST" + digits.zfill(4)

def vincular_ativos_handler(vinculos: List[AssetInput] = Body(...)):
    if not vinculos:
        raise HTTPException(status_code=400, detail="Lista de vínculos vazia.")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "asset_tag"])
        for item in vinculos:
            username = item.username.strip().lower()
            tag = _format_asset_tag(item.asset_tag.strip())
            writer.writerow([username, tag])

    return {"message": f"{len(vinculos)} vínculos registrados com sucesso."}

def exportar_ativos_handler():
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="Nenhum vínculo encontrado.")
    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }
    return FileResponse(
        CSV_PATH,
        media_type="text/csv",
        filename="transferencias.csv",  # nome correto
        headers=headers,
    )
