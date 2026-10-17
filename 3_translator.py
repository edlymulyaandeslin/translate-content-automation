#!/usr/bin/env python

from utilities.utils import read_from_csv, delay, log_progress
from config.c_selenium import By, create_driver, wait_for_element
from pathlib import Path

import pandas as pd


driver = create_driver()

def translate_language(title, description, language, attribs_col):
    try:
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
        
        return df, True
    except Exception as e:
        return [], False

def load_to_csv(df):
    df.to_csv("./results/data_source.csv", index=False)
    
def read_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        transcript = file.read().split("\n||")
    
    return transcript

###############################################################
# Main Function
###############################################################

languages = read_from_csv("./results/languages.csv")

transcript = read_from_txt("./transcript.txt")

title = transcript[0]
description = transcript[1]
attribs_col = ["lang", "lang_code", "title", "description"]


file_path = Path("./results/data_source.csv")

if file_path.exists():
    df_result = pd.read_csv(file_path)
else:
    df_result = pd.DataFrame(columns=attribs_col)

exists_lang = set(df_result['lang_code'].dropna())

log_progress("Start Transleting!")
for lang in languages.itertuples():
    if lang.code == "en" or lang.code in exists_lang or lang.Index > 100:
        continue

    log_progress(f"{lang.Index + 1} - translating to {lang.language_name} language")
    df_translate, success = translate_language(title, description, lang, attribs_col)

    if not success:
        continue

    df_result = pd.concat([df_result, df_translate], ignore_index=True)
    
    if (lang.Index > 10) and (lang.Index % 2 == 0):
        load_to_csv(df_result)

log_progress("Translation content completed!")

driver.quit()