# routes/login.py
from fastapi import APIRouter, HTTPException
from db import users_coll
from utils.security import verify_password
from utils.jwt import create_access_token

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/")
def login(email: str, password: str):
    user = users_coll.find_one({"email": email, "is_active": True})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": str(user["_id"]),  # 🔥 FIX
        "role": user["role"]
    })

    return {
        "access_token": token,
        "role": user["role"]
    }

