#!/usr/bin/env python

from config.c_selenium import By, create_driver, wait_for_element, wait_and_click
from utilities.utils import read_from_csv, log_progress, delay

driver = create_driver()

def upload_lang(driver, url, data):
    try:
        title = data.title[:100]
        description = data.description
        lang_code = data.lang_code
        lang = data.lang
        
        driver.get(url)
        
        delay()
        
        btn_add_lang = wait_and_click(driver, By.CSS_SELECTOR, "button[aria-label='Tambahkan bahasa']")
        log_progress(f"-- Tombol [{btn_add_lang.text}] di klik!")

        paper_list = wait_for_element(driver, By.ID, "paper-list")
        log_progress("-- paper_list bahasa ditemukan")

        selected_lang = paper_list.find_element(By.CSS_SELECTOR, f"[test-id='{lang_code}']")
        
        log_progress(f"-- Scroll to [{lang}] language!")
        driver.execute_script("""
            const el = arguments[0];
            let parent = el.parentElement;

            while (parent) {
                if (parent.scrollHeight > parent.clientHeight) {
                    parent.scrollTop =
                        el.getBoundingClientRect().top -
                        parent.getBoundingClientRect().top +
                        parent.scrollTop;

                    break;
                }
                parent = parent.parentElement;
            }
        """, selected_lang)
        
        delay(1, 2)
        
        log_progress(f"-- [{lang}] language diklik!")
        selected_lang.click()
        
        delay(2, 4)
        
        title_container = wait_for_element(driver, By.CLASS_NAME, "ytgnLanguageDialogMetadataTitle")
        input_title = title_container.find_element(By.ID, "textbox")
        delay(1, 1)
        log_progress(f"-- Input title")
        input_title.send_keys(title)
        
        delay(2, 4)
        
        log_progress(f"-- Input description")
        desc_container = wait_for_element(driver, By.CLASS_NAME, "ytgnLanguageDialogMetadataDescription")
        input_desc = desc_container.find_element(By.ID, "textbox")
        delay(1, 1)
        input_desc.send_keys(description)
        
        delay(2, 4)
        
        # klik perbarui
        log_progress(f"-- Perbarui di klik!")
        wait_and_click(driver, By.CSS_SELECTOR, "button[aria-label='Perbarui']")
        
        delay()
        return True
    except Exception as e:
        log_progress(f"-- ERROR element {lang}. error: {e}")
        return False

url = "https://studio.youtube.com/video/0q1m4sEtG0w/translations"

log_progress("Read data source")
data_source = read_from_csv("./results/data_source.csv")

log_progress("Read exists data source")
is_available = read_from_csv("./results/lang_available.csv")
available_langs = set(is_available["lang"].dropna())

for data in data_source.itertuples():
    if data.lang in available_langs:
        continue
    
    log_progress(f"{data.Index + 1} - Uploading [{data.lang}]")
    success = upload_lang(driver, url, data)
    
    delay()
    
    if not success:
        continue

log_progress("Uploaded content in many lang completed!")

driver.quit()