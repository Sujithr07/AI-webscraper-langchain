import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time

def scrape_web(website):
    print("launching chrome browser...")

    chrome_driver_path= ""
    options= webdriver.ChromeOptions()
    driver= webdriver.chrome(service= Service(chrome_driver_path),options=options)

    try:
        driver.get(website)
        print("page loaded...")
        html= driver.page_source

        return html
    finally:
        driver.quit()