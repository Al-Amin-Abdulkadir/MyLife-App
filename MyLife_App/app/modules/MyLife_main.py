from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import jwt
import json
import logging

from app.modules.MyLife_Tracker import (
    create_access_token as tracker_create_access_token,
    decode_access_token as tracker_decode_access_token,
    get_current_user_from_token as tracker_get_current_user_from_token,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("MyLife_main.py")
main_db = Path(__file__).resolve().parents[2] / "data" / "mylife.json"

def load_database():
    with open(main_db, "r")as file:
        return json.load(file)
    
def save_database(data):
    with open(main_db, "w") as file:
        json.dump(data, file, indent=4)

def create_access_token(user : dict) -> str:
    return tracker_create_access_token(user)

def decode_access_token(token : str) -> str:
    return tracker_decode_access_token(token)

def get_curent_user_from_token(token : str) -> dict | None:
    return tracker_get_current_user_from_token(token)

DXB_TZ = ZoneInfo("Asia/Dubai")
DXB_now = datetime.now(DXB_TZ)
print(DXB_now.isoformat(timespec="seconds"))

def dubai_now():
    return datetime.now(ZoneInfo("Asia/Dubai")).isoformat(timespec="seconds")
app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
