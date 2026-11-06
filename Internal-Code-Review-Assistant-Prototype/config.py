import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    DATABASE = os.getenv("DATABASE_PATH", str(BASE_DIR / "instance" / "reviews.db"))
