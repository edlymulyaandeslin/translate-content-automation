#!/usr/bin/env python

from utils import read_from_csv, delay, log_progress
from selenium_config import By, driver, wait_for_element

import pandas as pd

def translate_language(title, description, language, attribs_col):
    lang_code = language.code

    translate_url = f"https://translate.google.co.id/?sl=en&tl={lang_code}&op=translate"

    driver.get(translate_url) 
    
    delay()
    
    text_area = wait_for_element(driver, By.CLASS_NAME, "er8xn")
    text_area.send_keys(title)
    
    delay(2, 3)
    
    result_title = wait_for_element(driver, By.CLASS_NAME, "HwtZe").text
    text_area.clear()
    
    delay(1, 2)
    
    text_area.send_keys(description)

    delay(3, 4)
    
    result_desc = wait_for_element(driver, By.CLASS_NAME, "HwtZe").text

    data_dict = {
        "lang": language.language_name,
        "lang_code": lang_code,
        "title": result_title,
        "description": result_desc
    }
    
    df = pd.DataFrame([data_dict], columns=attribs_col)
    
    return df

def load_to_csv(df):
    df.to_csv("./data_source.csv")
    
def read_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        transcript = file.read().split("\n||")
        
    return transcript

###############################################################
# Main Function
###############################################################

languages = read_from_csv("./languages.csv")

transcript = read_from_txt("./transcript.txt")

title = transcript[0]
description = transcript[1]
attribs_col = ["lang", "lang_code", "title", "description"]

df_result = pd.DataFrame(columns=attribs_col)

log_progress("Start Transleting!")
for lang in languages.itertuples():
    if lang.code == "en":
        continue

    log_progress(f"Process translating to {lang.language_name}")
    
    df_translate = translate_language(title, description, lang, attribs_col)

    df_result = pd.concat([df_result, df_translate], ignore_index=True)
    
    if (lang.Index > 10) and (lang.Index % 2 == 0):
        load_to_csv(df_result)

log_progress("Translation content completed!")
print("="*50)
print(df_result.head())

driver.close()