import selenium.webdriver as webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, InvalidArgumentException
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

def scrape_web(website, clean=True, timeout=15):
    """Scrape website with error handling and timeout protection.
    
    Args:
        website: URL to scrape
        clean: Whether to clean HTML content
        timeout: Maximum time to wait for page load in seconds
    
    Returns:
        Cleaned or raw HTML content
    """
    # Validate URL
    if not website or not website.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL. Must start with http:// or https://")
    
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

    chrome_driver_path = "./chromedriver.exe"
    options = Options()
    options.set_capability("goog:chromeOptions", {"w3c": True})
    
    if proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")
    
    driver = None
    try:
        driver = WebDriver(service=Service(chrome_driver_path), options=options)
        driver.set_page_load_timeout(timeout)
        
        print(f"Navigating to {website}...")
        driver.get(website)
        time.sleep(3)  
        print("page loaded...")
        html = driver.page_source
        
        if clean:
            print("cleaning DOM content...")
            html = clean_html(html)

        return html
    
    except TimeoutException:
        print(f"Error: Page load timeout after {timeout} seconds")
        raise TimeoutException(f"Failed to load {website} within {timeout} seconds")
    except InvalidArgumentException as e:
        print(f"Error: Invalid URL - {e}")
        raise ValueError(f"Invalid URL: {website}")
    except WebDriverException as e:
        print(f"Error: WebDriver error - {e}")
        raise RuntimeError(f"Browser error while accessing {website}: {str(e)}")
    except Exception as e:
        print(f"Error: Unexpected error - {e}")
        raise RuntimeError(f"Failed to scrape {website}: {str(e)}")
    finally:
        if driver:
            driver.quit()