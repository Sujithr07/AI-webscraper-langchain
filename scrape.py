import selenium.webdriver as webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_web(website):
    print("launching chrome browser with Bright Data proxy...")

    # Bright Data credentials from environment variables
    proxy_user = os.getenv("BRIGHT_DATA_USER")
    proxy_pass = os.getenv("BRIGHT_DATA_PASS")
    proxy_host = "zproxy.lum-superproxy.io"
    proxy_port = 22225
    
    if not proxy_user or not proxy_pass:
        print("Warning: Bright Data credentials not found in .env file")
        proxy_url = None
    else:
        # Format proxy URL
        proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    chrome_driver_path= "./chromedriver.exe"
    options= Options()
    
    if proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")
    
    driver= WebDriver(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        time.sleep(3)  # Wait for page to render
        print("page loaded...")
        html= driver.page_source

        return html
    finally:
        driver.quit()