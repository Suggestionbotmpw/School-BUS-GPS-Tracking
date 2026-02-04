from fastapi import Depends, HTTPException, Header, Request
from typing import Optional, List
from bson import ObjectId

from utils.jwt import decode_access_token
from db import users_coll


def get_current_user(
    request: Request,
    authorization: Optional[str] = Header(None)
):
    print("AUTH HEADER:", authorization)

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "").strip()
    payload = decode_access_token(token)

    print("JWT PAYLOAD:", payload)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    print("USER ID:", user_id)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = users_coll.find_one({"_id": ObjectId(user_id), "is_active": True})
    print("DB USER:", user)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def role_required(allowed_roles: List[str]):
    def checker(current_user=Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not allowed")
        return current_user
    return checker
