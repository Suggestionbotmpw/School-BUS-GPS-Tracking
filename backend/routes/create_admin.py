from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel, EmailStr

from db import users_coll
from utils.security import hash_password
from roles import role_required

router = APIRouter(prefix="/super-admin", tags=["Super Admin"])


# ✅ Request schema
class CreateAdminRequest(BaseModel):
    institute_name: str 
    email: EmailStr
    phone: str
    password: str


@router.post("/create-admin")
def create_admin(
    data: CreateAdminRequest,
    super_admin=Depends(role_required(["super_admin"]))
):
    # 🔒 Check if admin already exists
    if users_coll.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Admin already exists")

    user_id = users_coll.insert_one({
        "name": data.institute_name,
        "email": data.email,
        "phone": data.phone,
        "password": hash_password(data.password),
        "role": "admin",
        "created_by": super_admin["_id"],   # ✅ FIXED
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }).inserted_id

    return {
        "message": "Admin created successfully",
        "admin_id": str(user_id)
    }
