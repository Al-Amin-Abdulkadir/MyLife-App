#Finance tracker for MyLife app
import re
import hashlib
import string
from wonderwords import random_word
import json
from pathlib import Path
from datetime import datetime, date
from zoneinfo import ZoneInfo
import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable
from MyLife_Tracker import * 

feature_db = Path(__file__).with_name("MyFinance_database_file.json")

def load_database():
    with open(feature_db, "r") as file:
        return json.load(file)
    
def save_database(data):
    with open(feature_db, "w") as file:
        json.dump(data, file, indent=4)

def user_special_key():
    r = RandomWord()
    special_key = r.word(word_min_length=5, word_max_length=5)
    return special_key
