import os
import csv
from typing import List, Optional
from collections import Counter
from fastapi import HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel

CSV_PATH = os.path.join("storage", "transferencias.csv")
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

class AssetInput(BaseModel):
    username: str
    asset_tag: str
    flag: Optional[str] = None

def vincular_ativos_handler(vinculos: List[AssetInput] = Body(...)):
    if not vinculos:
        raise HTTPException(status_code=400, detail="Lista de vínculos vazia.")

    tags_upper = [v.asset_tag.strip().upper() for v in vinculos]
    counts = Counter(tags_upper)
    
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "asset_tag", "flag"])
        for item in vinculos:
            username = item.username.strip().lower()
            tag = item.asset_tag.strip().upper()
            flag = (item.flag or "")
            if counts[tag] > 1 and not flag:
                flag = "DUPLICATE"
            writer.writerow([username, tag, flag])

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
