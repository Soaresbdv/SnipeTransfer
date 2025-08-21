from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ldap/search")
def ldap_autocomplete(term: str = Query(..., min_length=2)):
    fake_users = [
        {"username": "bruno.silva", "name": "Bruno Silva"},
        {"username": "beatriz.cemiauskas", "name": "Beatriz Cemiauskas"},
        {"username": "rafael.zelak", "name": "Rafael Zelak"},
    ]

    filtered = [
        user for user in fake_users
        if term.lower() in user["username"].lower() or term.lower() in user["name"].lower()
    ]

    return JSONResponse(filtered)