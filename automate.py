import urllib.parse
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Config
from logger import logger
from data_loader import load_contacts
from templater import format_message
from validator import clean_phone_number
from scheduler import RateLimiter

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
        
    # Add options to avoid bot detection fingerprints
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    
    # Set page load timeout
    timeout = config.get("browser", "page_load_timeout", default=30)
    driver.set_page_load_timeout(timeout)
    
    return driver

def run_campaign(cli_args=None):
    # 1. Load Settings
    config_path = cli_args.config if cli_args and cli_args.config else "config.yaml"
    config = Config(config_path)
    
    # Apply CLI overrides
    if cli_args:
        if cli_args.input:
            config.settings["campaign"]["input_file"] = cli_args.input
        if cli_args.message:
            config.settings["campaign"]["default_message"] = cli_args.message
        if cli_args.dry_run is not None:
            config.settings["campaign"]["dry_run"] = cli_args.dry_run
        if cli_args.headless is not None:
            config.settings["browser"]["headless"] = cli_args.headless
    
    input_file = config.get("campaign", "input_file")
    default_template = config.get("campaign", "default_message")
    country_code = config.get("campaign", "default_country_code")
    dry_run = config.get("campaign", "dry_run", default=False)
    
    logger.info(f"🚀 Starting WhatsApp Automation campaign using {input_file}...")
    
    # 2. Load Contacts
    contacts = load_contacts(input_file)
    if not contacts:
        logger.error("No contacts found. Exiting.")
        return
        
    # 3. Setup Scheduler/RateLimiter
    rate_limiter = RateLimiter(config)
    
    driver = None
    if not dry_run:
        # 4. Initialize Selenium Browser
        try:
            driver = setup_browser(config)
            driver.get("https://web.whatsapp.com")
            logger.info("👉 Scan QR code on WhatsApp Web, then press Enter in terminal...")
            input("Scan QR code and press ENTER to start sending messages...")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            if driver:
                driver.quit()
            return
    else:
        logger.info("ℹ️ Running in DRY-RUN mode. No messages will be sent.")

    # 5. Loop Through Contacts
    for index, contact in enumerate(contacts, 1):
        # Extract name and phone from row keys (case-insensitive checks)
        name = contact.get("Name") or contact.get("name") or "Recipient"
        raw_phone = contact.get("Phone") or contact.get("phone") or ""
        
        # Clean and Validate Phone Number
        phone = clean_phone_number(raw_phone, default_country_code=country_code)
        if not phone:
            logger.warning(f"⏩ Row {index}: Skipped due to invalid/missing phone number: {raw_phone}")
            continue
            
        # Compile Message Template
        # If the contact dictionary doesn't have "Name" explicitly, put the name we resolved
        contact_ctx = contact.copy()
        if "Name" not in contact_ctx and "name" not in contact_ctx:
            contact_ctx["Name"] = name
            
        message = format_message(default_template, contact_ctx)
        
        logger.info(f"Processing row {index}: {name} ({phone})")
        
        if dry_run:
            logger.info(f"[DRY-RUN] Would send to {name} ({phone}): \"{message}\"")
            continue
            
        # Send message via Selenium
        try:
            # Safe URL encoding of the message
            encoded_message = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
            logger.info(f"Opening conversation with {name}...")
            driver.get(url)
            
            # Wait for text box to load
            wait = WebDriverWait(driver, 30)
            input_box = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Add short delay before hitting Enter to look human
            import time
            time.sleep(1.5)
            
            input_box.send_keys(Keys.ENTER)
            logger.info(f"✅ Message sent to {name} ({phone})")
            
        except Exception as e:
            logger.error(f"❌ Failed to send to {name} ({phone}): {e}")
            
        # Anti-ban delay
        if index < len(contacts):
            rate_limiter.wait_between_messages()

    if driver:
        driver.quit()
    logger.info("🎉 Campaign completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WA_Automate: Professional WhatsApp Automation CLI tool.")
    parser.add_argument("-i", "--input", help="Path to contacts input file (CSV/Excel).")
    parser.add_argument("-m", "--message", help="Default message template.")
    parser.add_argument("-c", "--config", help="Path to YAML configuration file.")
    parser.add_argument("-d", "--dry-run", action="store_true", default=None, help="Run without sending messages.")
    parser.add_argument("--headless", action="store_true", default=None, help="Run Chrome browser in headless mode.")
    args = parser.parse_args()
    
    run_campaign(args)