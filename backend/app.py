from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from pathlib import Path
import os

from src.routes.assign_asset import vincular_ativos_handler, exportar_ativos_handler
from src.routes.ldap_search import router as ldap_router 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/assign", tags=["assign"])
router.add_api_route("/vincular-ativos", vincular_ativos_handler, methods=["POST"])
router.add_api_route("/exportar-ativos", exportar_ativos_handler, methods=["GET"])
app.include_router(router)
app.include_router(ldap_router) 

BASE_DIR = Path(__file__).resolve().parent.parent  
FRONTEND_DIR = BASE_DIR / "frontend"
TEMPLATES_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(TEMPLATES_DIR / "index.html")

app.mount("/scripts", StaticFiles(directory=STATIC_DIR / "scripts"), name="scripts")
app.mount("/styles", StaticFiles(directory=STATIC_DIR / "styles"), name="styles")
