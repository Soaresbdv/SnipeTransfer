import os
import csv
from typing import List
from fastapi import HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel

CSV_PATH = os.path.join("storage", "transferencias.csv")
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

class AssetInput(BaseModel):
    username: str
    asset_tag: str

def vincular_ativos_handler(vinculos: List[AssetInput] = Body(...)):
    if not vinculos:
        raise HTTPException(status_code=400, detail="Lista de vínculos vazia.")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "asset_tag"])
        for item in vinculos:
            writer.writerow([item.username.strip().lower(), item.asset_tag.strip().upper()])

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
        filename="transferencias.csv",
        headers=headers,
    )
