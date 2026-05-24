import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import Config
from .logger import logger
from .data_loader import load_contacts
from .templater import format_message
from .validator import clean_phone_number
from .scheduler import RateLimiter
from .driver import setup_browser, send_attachment
from .reporter import CampaignReporter

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
        if getattr(cli_args, "attachment", None):
            config.settings["campaign"]["attachment"] = cli_args.attachment
    
    input_file = config.get("campaign", "input_file")
    default_template = config.get("campaign", "default_message")
    country_code = config.get("campaign", "default_country_code")
    dry_run = config.get("campaign", "dry_run", default=False)
    attachment_path = config.get("campaign", "attachment")
    
    logger.info(f"🚀 Starting WhatsApp Automation campaign using {input_file}...")
    
    # 2. Load Contacts
    contacts = load_contacts(input_file)
    if not contacts:
        logger.error("No contacts found. Exiting.")
        return
        
    # 3. Setup Scheduler/RateLimiter
    rate_limiter = RateLimiter(config)
    reporter = CampaignReporter()
    
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
        logger.info("ℹ️ Running in DRY-RUN mode. Validating campaign details...")
        valid_count = 0
        invalid_count = 0
        for contact in contacts:
            raw_phone = contact.get("Phone") or contact.get("phone") or ""
            phone = clean_phone_number(raw_phone, default_country_code=country_code)
            if phone:
                valid_count += 1
            else:
                invalid_count += 1
        
        # Calculate estimate duration
        avg_delay = (rate_limiter.min_delay + rate_limiter.max_delay) / 2
        total_delays = avg_delay * max(0, valid_count - 1)
        # Add batch cooldowns
        batches = max(0, valid_count - 1) // rate_limiter.batch_size
        total_cooldowns = batches * rate_limiter.batch_cooldown
        est_seconds = total_delays + total_cooldowns
        est_minutes = est_seconds / 60
        
        logger.info("=== DRY-RUN CAMPAIGN SUMMARY ===")
        logger.info(f"Loaded Contacts: {len(contacts)}")
        logger.info(f"Valid Phone Numbers: {valid_count}")
        logger.info(f"Invalid Phone Numbers: {invalid_count}")
        logger.info(f"Estimated Campaign Duration: {est_minutes:.1f} minutes")
        logger.info("=================================")

    # 5. Loop Through Contacts
    index = 0
    while index < len(contacts):
        contact = contacts[index]
        row_num = index + 1
        name = contact.get("Name") or contact.get("name") or "Recipient"
        raw_phone = contact.get("Phone") or contact.get("phone") or ""
        
        try:
            phone = clean_phone_number(raw_phone, default_country_code=country_code)
            if not phone:
                logger.warning(f"⏩ Row {row_num}: Skipped due to invalid/missing phone number: {raw_phone}")
                reporter.log_result(row_num, name, raw_phone, "SKIPPED", "Invalid or missing phone number.")
                index += 1
                continue
                
            contact_ctx = contact.copy()
            if "Name" not in contact_ctx and "name" not in contact_ctx:
                contact_ctx["Name"] = name
                
            message = format_message(default_template, contact_ctx)
            
            if dry_run:
                logger.info(f"[DRY-RUN] Success for {name} ({phone}) → Message: \"{message}\"")
                if attachment_path:
                    logger.info(f"[DRY-RUN] Success for {name} ({phone}) → Would send attachment: {attachment_path}")
                reporter.log_result(row_num, name, phone, "DRY_RUN", f"Mocked message send. Template: {message}")
                index += 1
                continue
                
            logger.info(f"Processing row {row_num}: {name} ({phone})")
            
            # Send message via Selenium
            try:
                encoded_message = urllib.parse.quote(message)
                url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
                logger.info(f"Opening conversation with {name}...")
                driver.get(url)
                
                wait = WebDriverWait(driver, 30)
                input_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                
                time.sleep(1.5)
                input_box.send_keys(Keys.ENTER)
                logger.info(f"✅ Message sent to {name} ({phone})")
                
                if attachment_path:
                    time.sleep(2.0)
                    send_attachment(driver, attachment_path)
                
                reporter.log_result(row_num, name, phone, "SUCCESS")
                
            except Exception as e:
                logger.error(f"❌ Failed to send to {name} ({phone}): {e}")
                reporter.log_result(row_num, name, phone, "FAILED", str(e))
                
            if row_num < len(contacts):
                rate_limiter.wait_between_messages()
            
            index += 1

        except KeyboardInterrupt:
            logger.warning("\n⏸️ Campaign paused by user interrupt (Ctrl+C).")
            choice = input("Press [Enter] to resume, or type 'exit' to save report and terminate: ").strip().lower()
            if choice == 'exit':
                logger.info("Terminating campaign. Saving report...")
                break
            else:
                logger.info("Resuming campaign...")
                continue

    if driver:
        driver.quit()
    
    # Generate CSV Report
    reporter.generate_report()
    logger.info("🎉 Campaign completed successfully.")
