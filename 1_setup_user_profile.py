#!/usr/bin/env python

from pathlib import Path
import subprocess, psutil
from utilities.utils import root_dir

BASE_DIR = root_dir(Path(__file__))
PROFILE_DIR = BASE_DIR / "profiles" / "e09_yt"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PROFILE_DIR.mkdir(parents=True, exist_ok=True)

process = subprocess.Popen([
    CHROME_PATH,
    f"--user-data-dir={PROFILE_DIR}"
])

input("Tekan ENTER untuk menutup chrome..")

parent = psutil.Process(process.pid)
processes = parent.children(recursive=True)

for proc in processes:
    proc.terminate()

parent.terminate()

psutil.wait_procs([parent, *processes], timeout=5)