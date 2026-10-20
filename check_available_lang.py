#!/usr/bin/env python

from config.c_selenium import By, create_driver, wait_for_all_element
from utilities.utils import load_to_csv, log_progress
import pandas as pd

driver = create_driver()

def extract_available(driver, url):
    try:
        driver.get(url)
        
        rows = wait_for_all_element(driver, By.CSS_SELECTOR, "td.tablecell-language")
        
        data = []
        
        for row in rows:
            lang = row.text
            
            data.append(lang)
        
        df = pd.DataFrame(data, columns=["lang"])
        
        return df
    except Exception as e:
        log_progress(f"Error: {e}")
        raise e

url = "https://studio.youtube.com/video/0q1m4sEtG0w/translations"

log_progress("Getting available language")
available_lang = extract_available(driver, url)
log_progress(f"Found {len(available_lang)} available language")

log_progress("Load to csv")
load_to_csv(available_lang, "lang_available.csv")
log_progress("Completed!")

driver.quit()