import argparse
from wa_automate import run_campaign

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WA_Automate: Professional WhatsApp Automation CLI tool.")
    parser.add_argument("-i", "--input", help="Path to contacts input file (CSV/Excel).")
    parser.add_argument("-m", "--message", help="Default message template.")
    parser.add_argument("-c", "--config", help="Path to YAML configuration file.")
    parser.add_argument("-d", "--dry-run", action="store_true", default=None, help="Run without sending messages.")
    parser.add_argument("--headless", action="store_true", default=None, help="Run Chrome browser in headless mode.")
    parser.add_argument("-a", "--attachment", help="Path to attachment file to send.")
    args = parser.parse_args()
    
    run_campaign(args)