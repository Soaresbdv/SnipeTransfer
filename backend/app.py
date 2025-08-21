from fastapi import FastAPI, APIRouter
from src.routes.assign_asset import vincular_ativos_handler, exportar_ativos_handler, AssetInput
from typing import List

app = FastAPI()

router = APIRouter(prefix="/assign", tags=["assign"])

router.add_api_route("/vincular-ativos", vincular_ativos_handler, methods=["POST"], response_model=None)
router.add_api_route("/exportar-ativos", exportar_ativos_handler, methods=["GET"])

app.include_router(router)
