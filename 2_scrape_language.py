#!/usr/bin/env python

from config.selenium import By, driver, wait_for_element, wait_and_click
from utilities.utils import delay, log_progress

import pandas as pd


def extract_language(url):
    driver.get(url)

    delay()
    
    btn_add_lang = wait_and_click(driver, By.CSS_SELECTOR, "button[aria-label='Tambahkan bahasa']")
    log_progress(f"Tombol {btn_add_lang.text} di klik!")

    paper_list = wait_for_element(driver, By.ID, "paper-list")
    log_progress("paper_list bahasa ditemukan!")

    elements = paper_list.find_elements(By.CSS_SELECTOR, ".tp-yt-paper-item.selectable-item")
    log_progress(f"Jumlah bahasa yang ditemukan: {len(elements)} bahasa")
    
    data = []
    for _, element in enumerate(elements):
        code = element.get_attribute("test-id") 
        language_name = element.text.strip()
        
        data_dict = {
            "code": code,
            "language_name": language_name
        }
        
        data.append(data_dict)
    
    df = pd.DataFrame(data, columns=["code", "language_name"])
    
    return df

def load_to_csv(df):
    df.to_csv("./results/languages.csv", index=False)


url = "https://studio.youtube.com/video/OnWzR2jy36I/translations"
try:
    log_progress("Extracting language!!")
    extracted_language = extract_language(url)

    log_progress("Load to CSV!!")
    load_to_csv(extracted_language)

finally:
    driver.quit()