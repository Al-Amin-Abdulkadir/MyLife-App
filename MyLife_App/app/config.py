from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://alamin@localhost/mylife_db")
SECRET_KEY = os.getenv("SECRET_KEY", "")