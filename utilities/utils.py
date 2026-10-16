
import json, time, random
import pandas as pd
from datetime import datetime
from pathlib import Path

def root_dir(path: Path):
    for parent in path.resolve().parents:
        if(parent / "requirements.txt").exists():
            return parent
    
    raise FileNotFoundError("Root directory tidak ditemukan")

def read_cookie_from_json():
    with open("../cookies.json", "r", encoding="utf-8") as file:
        data_cookie = json.load(file)
    
    return data_cookie

def read_from_csv(filepath):
    data = pd.read_csv(filepath)
    
    return data

def load_to_csv(df: pd.DataFrame, filepath):
    path = root_dir(Path(__file__))/f"results/{filepath}"
    df.to_csv(path, index=False)

def delay(start = 1, end = 3):
    if start > end:
        temp_start = start
        start = end
        end = temp_start
    
    time.sleep(random.uniform(start, end))

def log_progress(message):
    path = root_dir(Path(__file__)) / "log/log.txt"
    timestamp = f"%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    dateformat = now.strftime(timestamp)
    with open(path, "a") as logfile:
        logfile.write(f"{dateformat}: {message}\n")
    
    print(f"{dateformat}: {message}")