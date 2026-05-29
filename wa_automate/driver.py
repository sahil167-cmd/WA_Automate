import os
import time
from typing import Any
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .logger import logger
from .config import Config
from .exceptions import BrowserDriverError, ValidationError

MAX_ATTACHMENT_SIZE_MB = 100  # Default max limit of 100MB for documents on WhatsApp Web


def setup_browser(config: Config) -> webdriver.Chrome:
    """Initialize and configure Chrome WebDriver based on configuration."""
    logger.info("Initializing Chrome WebDriver...")
    options = webdriver.ChromeOptions()
    
    # Configure Headless Mode
    if config.get("browser", "headless", default=False):
        options.add_argument("--headless=new")
        # Headless Chrome requires a standard user agent to bypass WhatsApp Web blocks
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--window-size=1920,1080")
        logger.info("Running browser in headless mode with user-agent spoofing.")
        
    # Configure Start Maximized
    if config.get("browser", "maximize", default=True) and not config.get("browser", "headless", default=False):
        options.add_argument("--start-maximized")
        
    # Configure Session Persistence
    user_data_dir = config.get("browser", "user_data_dir")
    if user_data_dir:
        abs_data_dir = os.path.abspath(user_data_dir)
        options.add_argument(f"user-data-dir={abs_data_dir}")
        logger.info(f"Using Chrome user profile for session persistence: {abs_data_dir}")
        
    # Add options to avoid bot detection fingerprints
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        raise BrowserDriverError(f"Failed to create Chrome WebDriver instance: {e}") from e
    
    # Set page load timeout
    timeout = config.get("browser", "page_load_timeout", default=30)
    driver.set_page_load_timeout(timeout)
    
    return driver


def send_attachment(driver: webdriver.Chrome, file_path: str) -> bool:
    """
    Uploads and sends an attachment file (image, video, document) via WhatsApp Web.
    Performs file existence, directory and size validation.
    Returns True if successful, False otherwise.
    """
    if not file_path:
        logger.error("Attachment path is empty.")
        return False

    if not os.path.exists(file_path):
        logger.error(f"Attachment file not found: {file_path}")
        return False

    if os.path.isdir(file_path):
        logger.error(f"Attachment path is a directory, not a file: {file_path}")
        return False

    # Check file size (E.g. WhatsApp limits)
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        if size_mb > MAX_ATTACHMENT_SIZE_MB:
            logger.error(f"Attachment size ({size_mb:.2f}MB) exceeds maximum limit of {MAX_ATTACHMENT_SIZE_MB}MB.")
            return False
    except Exception as e:
        logger.warning(f"Could not verify file size for '{file_path}': {e}")
        
    abs_path = os.path.abspath(file_path)
    logger.info(f"Uploading attachment: {abs_path}")
    try:
        wait = WebDriverWait(driver, 20)
        file_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(abs_path)
        
        # Wait for the send button on the preview screen to appear and click it
        send_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]/parent::button | //div[@aria-label="Send"][@role="button"]'))
        )
        
        time.sleep(2.0)  # Allow time for upload preview loading
        send_btn.click()
        logger.info(f"✅ Attachment sent: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send attachment: {e}")
        return False
