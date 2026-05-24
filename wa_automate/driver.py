from selenium import webdriver
from .logger import logger
from .config import Config

def setup_browser(config: Config):
    """Initialize and configure Chrome WebDriver based on configuration."""
    logger.info("Initializing Chrome WebDriver...")
    options = webdriver.ChromeOptions()
    
    # Configure Headless Mode
    if config.get("browser", "headless", default=False):
        options.add_argument("--headless=new")
        logger.info("Running browser in headless mode.")
        
    # Configure Start Maximized
    if config.get("browser", "maximize", default=True):
        options.add_argument("--start-maximized")
        
    # Configure Session Persistence
    user_data_dir = config.get("browser", "user_data_dir")
    if user_data_dir:
        import os
        abs_data_dir = os.path.abspath(user_data_dir)
        options.add_argument(f"user-data-dir={abs_data_dir}")
        logger.info(f"Using Chrome user profile for session persistence: {abs_data_dir}")
        
    # Add options to avoid bot detection fingerprints
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    
    # Set page load timeout
    timeout = config.get("browser", "page_load_timeout", default=30)
    driver.set_page_load_timeout(timeout)
    
    return driver

def send_attachment(driver, file_path):
    """
    Uploads and sends an attachment file (image, video, document) via WhatsApp Web.
    Returns True if successful, False otherwise.
    """
    import os
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    if not os.path.exists(file_path):
        logger.error(f"Attachment file not found: {file_path}")
        return False
        
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
