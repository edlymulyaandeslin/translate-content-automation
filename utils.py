
import json, time, random
import pandas as pd
from datetime import datetime

def read_cookie_from_json():
    with open("./cookies.json", "r", encoding="utf-8") as file:
        data_cookie = json.load(file)
    
    return data_cookie

def read_from_csv(filepath):
    data = pd.read_csv(filepath)
    
    return data

def delay(start = 1, end = 3):
    if start > end:
        temp_start = start
        start = end
        end = temp_start
    
    time.sleep(random.uniform(start, end))

def log_progress(message):
    timestamp = f"%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    dateformat = now.strftime(timestamp)
    with open("./log.txt", "a") as logfile:
        logfile.write(f"{dateformat}: {message}\n")
    
    print(f"{dateformat}: {message}")