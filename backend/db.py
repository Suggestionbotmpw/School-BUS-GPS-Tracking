import os
from pymongo import MongoClient
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# CONFIG (ONLY TWO VARS)
# =========================
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("AUTH_DB_NAME")

# =========================
# SAFETY CHECKS
# =========================
if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI missing in .env")

if not DB_NAME:
    raise RuntimeError("❌ AUTH_DB_NAME missing in .env")

if not (
    MONGO_URI.startswith("mongodb://")
    or MONGO_URI.startswith("mongodb+srv://")
):
    raise RuntimeError(f"❌ Invalid MONGO_URI: {MONGO_URI}")

print("🔹 Connecting to MongoDB Atlas:", MONGO_URI)

# =========================
# CONNECTION
# =========================
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
client.admin.command("ping")

db = client[DB_NAME]

print(f"✅ MongoDB connected | DB = {DB_NAME}")

# =========================
# COLLECTIONS (ALL IN SAME DB)
# =========================
users_coll = db["users"]
auth_coll = db["roles"]
token_blocklist = db["token_blocklist"]
