import time
import pandas as pd
from src.api import get_users, get_user_assets

# Função para auditar usuários com ativos duplicados e retornar um CSV
def audit_duplicates(out_path="duplicate_active_users.csv"):
    rows = []
    for user in get_users():
        cats = {}
        for asset in get_user_assets(user["id"]):
            cat = asset.get("category", {}).get("name", "Desconhecido")
            tag = asset.get("asset_tag", "N/A")
            cats.setdefault(cat, []).append(tag)
        for c, tags in cats.items():
            if len(tags) > 1:
                rows.append({
                    "username": user["username"],
                    "full_name": user.get("name", ""),
                    "category": c,
                    "quantidade": len(tags),
                    "asset_tags": ", ".join(tags)
                })
        time.sleep(0.5)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"✔️ Resultado salvo em {out_path}")

if __name__ == "__main__":
    audit_duplicates()