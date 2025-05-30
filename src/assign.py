import os
import time
import csv
from datetime import datetime
from src.api import assign_asset

# Atualizado: Agora o CSV vem da pasta TransferIn/
CSV_PATH = os.path.join("TransferIn", "transferencias.csv")

# Define nome do log com timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_PATH = os.path.join("logs", f"log_transferencias_{timestamp}.txt")

# Função para transferência de ativo
def process_transfers():
    successes = fails = 0

    print("🔄 Iniciando processo de transferências…")
    if not os.path.isfile(CSV_PATH):
        print(f"❌ Arquivo não encontrado: {CSV_PATH}")
        return

    with open(CSV_PATH, newline='', encoding='utf-8') as f, open(LOG_PATH, "a", encoding="utf-8") as log_file:
        reader = csv.DictReader(f)
        for row in reader:
            username = row.get("username", "").strip()
            asset_tag = row.get("asset_tag", "").strip()
            result = assign_asset(username, asset_tag)
            print(f"➡️  {result}")
            log_file.write(f"{result}\n")
            if "status" in result:
                successes += 1
            else:
                fails += 1
            time.sleep(2)

    print(f"\n✅ Transferências concluídas: {successes} sucesso(s), {fails} falha(s).")
    print(f"📝 Log salvo em: {LOG_PATH}")

if __name__ == "__main__":
    process_transfers()
