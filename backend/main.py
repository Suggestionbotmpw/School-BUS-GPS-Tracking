# =========================
# ENV
# =========================
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# =========================
# CORE FASTAPI
# =========================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =========================
# ROUTES
# =========================
from routes.login import router as login_router
from routes.create_admin import router as create_admin_router
from routes.admin_management import router as admin_management_router

# =========================
# STARTUP SEEDS
# =========================
from seed_roles import seed_roles   # ✅ roles only (safe to run always)

app = FastAPI(title="MySchoolBus API")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🔒 restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# STARTUP TASKS
# =========================
@app.on_event("startup")
def on_startup():
    seed_roles()   # ✅ idempotent

# =========================
# ROUTE REGISTRATION
# =========================
app.include_router(login_router)
app.include_router(create_admin_router)
app.include_router(admin_management_router)

# =========================
# HEALTH
# =========================
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "MySchoolBus Backend"
    }

# =========================
# DEBUG ROUTE (DEV ONLY)
# =========================
@app.get("/__routes")
def list_routes():
    return [
        {
            "path": route.path,
            "methods": list(getattr(route, "methods", [])),
            "name": route.name,
        }
        for route in app.router.routes
    ]
