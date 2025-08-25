from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routes.assign_asset import vincular_ativos_handler, exportar_ativos_handler
from src.routes.ldap_search import router as ldap_router

from dotenv import load_dotenv
from pathlib import Path
import os

# Carregar variáveis de ambiente do .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Instância principal do FastAPI
app = FastAPI()

# Middleware CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de rotas de API
router = APIRouter(prefix="/assign", tags=["assign"])
router.add_api_route("/vincular-ativos", vincular_ativos_handler, methods=["POST"])
router.add_api_route("/exportar-ativos", exportar_ativos_handler, methods=["GET"])
app.include_router(router)
app.include_router(ldap_router)

# Diretórios do frontend
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

# Servir HTML principal
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(TEMPLATES_DIR / "index.html")

# Servir arquivos estáticos (JS e CSS)
app.mount("/scripts", StaticFiles(directory=FRONTEND_DIR / "scripts"), name="scripts")
app.mount("/styles", StaticFiles(directory=FRONTEND_DIR / "styles"), name="styles")