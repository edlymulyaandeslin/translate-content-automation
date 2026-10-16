#!/usr/bin/env python

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utilities.utils import root_dir

BASE_DIR = root_dir(Path(__file__))

PROFILE_DIR = BASE_DIR / "chrome_profile"
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")

service = Service(executable_path=str(CHROMEDRIVER_PATH))

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://studio.youtube.com/")

    input("Setelah pesan muncul, tekan Enter...")

finally:
    driver.quit()