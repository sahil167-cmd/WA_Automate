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
