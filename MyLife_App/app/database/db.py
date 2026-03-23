import json
from pathlib import Path

from app.config import DATA_DIR


MYLIFE_DB = DATA_DIR / "mylife.json"
FITNESS_DB = DATA_DIR / "fitness.json"
FINANCE_DB = DATA_DIR / "finance.json"
CALENDAR_DB = DATA_DIR / "calendar.json"


def _load_json(path: Path, default: dict | list):
    if not path.exists():
        return default
    with open(path, "r") as file:
        return json.load(file)


def _save_json(path: Path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def load_mylife_data():
    return _load_json(MYLIFE_DB, {"users": []})


def save_mylife_data(data):
    _save_json(MYLIFE_DB, data)


def load_fitness_data():
    return _load_json(FITNESS_DB, {"meal_log": [], "meal_plans": [], "workout_sessions": [], "routines": []})


def save_fitness_data(data):
    _save_json(FITNESS_DB, data)


def load_finance_data():
    return _load_json(FINANCE_DB, {})


def save_finance_data(data):
    _save_json(FINANCE_DB, data)


def load_calendar_data():
    return _load_json(CALENDAR_DB, {})


def save_calendar_data(data):
    _save_json(CALENDAR_DB, data)

