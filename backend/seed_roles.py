# seed_roles.py
from db import auth_coll

DEFAULT_ROLES = [
    {"name": "super_admin"},
    {"name": "admin"},
    {"name": "driver"},
    {"name": "parents"},
]

def seed_roles():
    for role in DEFAULT_ROLES:
        auth_coll.update_one(
            {"name": role["name"]},
            {"$setOnInsert": role},
            upsert=True,
        )

    print("✅ Roles seeded")
