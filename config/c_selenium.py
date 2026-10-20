from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.utils import root_dir

BASE_DIR = root_dir(Path(__file__))
PROFILE_DIR = BASE_DIR / "profiles" / "e09_yt"

def create_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/155.0.0.0 Safari/537.36"
    )
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")

    return webdriver.Chrome(options=options)

# Selenium wait functions
def wait_for_all_element(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, value)))

def wait_for_element(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def wait_and_click(driver, by, value, timeout=15):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    element.click()
    return element
