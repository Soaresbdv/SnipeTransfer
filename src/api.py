import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

SNIPEIT_URL = os.getenv("SNIPEIT_URL")
SNIPEIT_TOKEN = os.getenv("SNIPEIT_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {SNIPEIT_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
STATUS_ID = 4  # "In Use" código do SnipeIT

user_cache = {}
asset_cache = {}

# Busca o usuário no Snipe-IT
def fetch_user(username):
    if username in user_cache:
        return user_cache[username]
    url = f"{SNIPEIT_URL}/api/v1/users?search={username}"
    while True:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            result = r.json()
            user_cache[username] = result
            return result
        elif r.status_code == 429:
            print(f"⚠️ Rate limit atingido ao buscar usuário '{username}', aguardando...")
            time.sleep(5)
        else:
            return {"error": r.text}
        
# Buscat o ativo no Snipe-IT
def fetch_asset(asset_tag):
    if asset_tag in asset_cache:
        return asset_cache[asset_tag]
    url = f"{SNIPEIT_URL}/api/v1/hardware?search={asset_tag}"
    while True:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            result = r.json()
            asset_cache[asset_tag] = result
            return result
        elif r.status_code == 429:
            print(f"⚠️ Rate limit atingido ao buscar ativo '{asset_tag}', aguardando...")
            time.sleep(5)
        else:
            return {"error": r.text}

# Associa um ativo a um usuário no Snipe-IT e retorna filtrado
def assign_asset(username, asset_tag):
    user = fetch_user(username)
    if "error" in user or not user.get("rows"):
        return {"username": username, "asset_tag": asset_tag,
                "error": f"Usuário '{username}' não encontrado."}

    asset = fetch_asset(asset_tag)
    if "error" in asset or not asset.get("rows"):
        return {"username": username, "asset_tag": asset_tag,
                "error": f"Ativo '{asset_tag}' não encontrado."}

    user_id = user["rows"][0]["id"]
    asset_id = asset["rows"][0]["id"]
    payload = {"assigned_user": user_id, "status_id": STATUS_ID}
    url = f"{SNIPEIT_URL}/api/v1/hardware/{asset_id}"

    while True:
        response = requests.put(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return {"username": username, "asset_tag": asset_tag, "status": "Transferência OK"}
        elif response.status_code == 429:
            print(f"⚠️ Rate limit atingido ao transferir ativo '{asset_tag}', aguardando...")
            time.sleep(5)
        else:
            return {"username": username, "asset_tag": asset_tag,
                    "error": f"Erro na transferência ({response.status_code})"}
