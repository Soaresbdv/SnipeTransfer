import os
import time
import json
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

SNIPEIT_URL = os.getenv("SNIPEIT_URL")
SNIPEIT_TOKEN = os.getenv("SNIPEIT_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {SNIPEIT_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
LIMIT = 50

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUT_PATH = os.path.join("logs", "where_asset", f"ativos_filtrados_{timestamp}.json")
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

def get_all_users():
    users = []
    offset = 0
    while True:
        url = f"{SNIPEIT_URL}/api/v1/users?limit={LIMIT}&offset={offset}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            result = r.json()
            users.extend(result.get("rows", []))
            if len(result.get("rows", [])) < LIMIT:
                break
            offset += LIMIT
        elif r.status_code == 429:
            print("⚠️ Rate limit atingido ao buscar usuários, aguardando...")
            time.sleep(5)
        else:
            print(f"❌ Erro ao buscar usuários: {r.status_code}")
            break
    return users

def get_user_assets(user_id):
    url = f"{SNIPEIT_URL}/api/v1/users/{user_id}/assets"
    while True:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("rows", [])
        elif r.status_code == 429:
            print(f"⚠️ Rate limit user_id={user_id}, aguardando...")
            time.sleep(5)
        else:
            print(f"❌ Erro ao buscar ativos do user_id={user_id}: {r.status_code}")
            return []

def process_assets_by_user():
    print("📦 Gerando JSON filtrado (username, name, category, etc)…")
    users = get_all_users()
    result = []

    for user in users:
        uid = user.get("id")
        username = user.get("username")
        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        assets_raw = get_user_assets(uid)

        assets_filtered = []
        for asset in assets_raw:
            assets_filtered.append({
                "id": asset.get("id"),
                "asset_tag": asset.get("asset_tag"),
                "serial": asset.get("serial"),
                "category": asset.get("category", {}).get("name", None)
            })

        result.append({
            "username": username,
            "name": full_name,
            "assets": assets_filtered
        })

        time.sleep(0.5)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON filtrado salvo em: {OUT_PATH}")

if __name__ == "__main__":
    process_assets_by_user()