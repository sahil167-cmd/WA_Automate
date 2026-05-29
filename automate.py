import argparse
import os
import pandas as pd
from wa_automate import run_campaign

def generate_sample_data(file_type: str = "xlsx") -> None:
    """Utility to generate a dummy contact list for testing."""
    sample_contacts = [
        {"Name": "John Doe", "Phone": "919876543210", "Company": "Acme Corp"},
        {"Name": "Jane Smith", "Phone": "918765432109", "Company": "Beta LLC"},
        {"Name": "Invalid Num", "Phone": "12345", "Company": "Delta Inc"}
    ]
    df = pd.DataFrame(sample_contacts)
    
    os.makedirs("templates", exist_ok=True)
    if file_type == "csv":
        path = os.path.join("templates", "contacts_template.csv")
        df.to_csv(path, index=False)
        print(f"Generated sample CSV contact file at: {path}")
    else:
        path = os.path.join("templates", "contacts_template.xlsx")
        df.to_excel(path, index=False, engine="openpyxl")
        print(f"Generated sample Excel contact file at: {path}")


def main():
    parser = argparse.ArgumentParser(description="WA_Automate: Professional WhatsApp Automation CLI tool.")
    parser.add_argument("-i", "--input", help="Path to contacts input file (CSV/Excel/JSON).")
    parser.add_argument("-m", "--message", help="Default message template.")
    parser.add_argument("-c", "--config", help="Path to YAML configuration file.")
    parser.add_argument("-d", "--dry-run", action="store_true", default=None, help="Run without sending messages.")
    parser.add_argument("--headless", action="store_true", default=None, help="Run Chrome browser in headless mode.")
    parser.add_argument("-a", "--attachment", help="Path to attachment file to send.")
    parser.add_argument(
        "--generate-template", 
        choices=["csv", "xlsx"], 
        help="Generate a dummy/sample contact file (CSV or Excel) under 'templates/' directory and exit."
    )
    
    args = parser.parse_args()
    
    if args.generate_template:
        generate_sample_data(args.generate_template)
        return
        
    run_campaign(args)


if __name__ == "__main__":
    main()