from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel

from db import users_coll
from utils.security import hash_password
from roles import role_required

router = APIRouter(prefix="/admin", tags=["Admin"])

# =========================
# DRIVER
# =========================
class CreateDriverRequest(BaseModel):
    driver_name: str
    driver_email: str
    driver_phone: str
    driver_password: str
    bus_number: str
    driver_last_point_address: str


@router.post("/create-driver")
def create_driver(
    data: CreateDriverRequest,
    admin=Depends(role_required(["admin"]))
):
    if not data.driver_email:
        raise HTTPException(status_code=400, detail="Driver email cannot be empty")

    if users_coll.find_one({"email": data.driver_email.strip()}):
        raise HTTPException(status_code=400, detail="Driver already exists")

    users_coll.insert_one({
        "name": data.driver_name.strip(),
        "email": data.driver_email.strip(),
        "phone": data.driver_phone.strip(),
        "password": hash_password(data.driver_password),
        "role": "driver",
        "bus_number": data.bus_number.strip(),
        "last_point_address": data.driver_last_point_address.strip(),
        "created_by": admin["_id"],
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })

    return {"message": "Driver created successfully"}


# =========================
# PARENT
# =========================
# =========================
# PARENT + STUDENT
# =========================
class CreateParentRequest(BaseModel):
    parent_name: str
    parent_email: str
    parent_phone: str
    parent_password: str

    student_name: str        # ✅ NEW
    student_standard: str
    student_address: str
    bus_number: str          # ✅ ADDED BY ADMIN


@router.post("/create-parent")
def create_parent(
    data: CreateParentRequest,
    admin=Depends(role_required(["admin"]))
):
    if not data.parent_email:
        raise HTTPException(status_code=400, detail="Parent email cannot be empty")

    if users_coll.find_one({"email": data.parent_email.strip()}):
        raise HTTPException(status_code=400, detail="Parent already exists")

    users_coll.insert_one({
        "name": data.parent_name.strip(),
        "email": data.parent_email.strip(),
        "phone": data.parent_phone.strip(),
        "password": hash_password(data.parent_password),
        "role": "parent",

        # ✅ STUDENT DETAILS STORED IN PARENT
        "student_name": data.student_name.strip(),
        "student_standard": data.student_standard.strip(),
        "student_address": data.student_address.strip(),
        "bus_number": data.bus_number.strip(),

        "created_by": admin["_id"],
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })

    return {"message": "Parent and student created successfully"}
