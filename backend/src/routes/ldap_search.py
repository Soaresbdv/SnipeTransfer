from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ldap3 import Server, Connection, ALL
import os

router = APIRouter(prefix="/ldap", tags=["ldap"])

@router.get("/search")
async def search_users(term: str = Query(..., min_length=1)):
    LDAP_SERVER = os.getenv("LDAP_SERVER")
    LDAP_USER = os.getenv("LDAP_USER")
    LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")
    LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")

    print("LDAP_SERVER:", LDAP_SERVER)
    print("LDAP_USER:", LDAP_USER)

    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)
    conn.search(
        search_base=LDAP_BASE_DN,
        search_filter=f"(&(objectClass=user)(sAMAccountName=*{term}*))",
        attributes=["sAMAccountName", "displayName"]
    )

    results = []
    for entry in conn.entries:
        sAM = entry.sAMAccountName.value
        display = entry.displayName.value
        if sAM and display and not sAM.endswith("$"):
            results.append({"username": sAM, "name": display})

    conn.unbind()
    return JSONResponse(content=results)