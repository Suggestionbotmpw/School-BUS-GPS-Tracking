from datetime import datetime
from db import users_coll
from utils.security import hash_password

SUPER_ADMIN = {
    "role": "super_admin",
    "name": "System Owner",
    "email": "superadmin@schoolbus.com",
    "phone": "9999999999",
    "password": hash_password("SuperAdmin@123"),
    "is_active": True,                 # ✅ REQUIRED
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
}

if users_coll.find_one({"role": "super_admin"}):
    print("❌ Super admin already exists")
else:
    users_coll.insert_one(SUPER_ADMIN)
    print("✅ Super admin created")
