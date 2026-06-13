import selenium.webdriver as webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()

def clean_html(html):
    """Remove scripts, styles, and extra whitespace from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    
    for script in soup(["script", "style", "meta", "link"]):
        script.decompose()
    
    for comment in soup.findAll(string=lambda text: isinstance(text, BeautifulSoup.Comment)):
        comment.extract()
    
    text = soup.get_text()
    
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def scrape_web(website, clean=True):
    print("launching chrome browser with Bright Data proxy...")

    proxy_user = os.getenv("BRIGHT_DATA_USER")
    proxy_pass = os.getenv("BRIGHT_DATA_PASS")
    proxy_host = "zproxy.lum-superproxy.io"
    proxy_port = 22225
    
    if not proxy_user or not proxy_pass:
        print("Warning: Bright Data credentials not found in .env file")
        proxy_url = None
    else:
        proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    chrome_driver_path= "./chromedriver.exe"
    options= Options()
    
    if proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")
    
    driver= WebDriver(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        time.sleep(3)  
        print("page loaded...")
        html= driver.page_source
        
        if clean:
            print("cleaning DOM content...")
            html = clean_html(html)

        return html
    finally:
        driver.quit()