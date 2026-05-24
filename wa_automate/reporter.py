import csv
import os
import datetime
from .logger import logger

class CampaignReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self.records = []
        os.makedirs(self.output_dir, exist_ok=True)

    def log_result(self, index, name, phone, status, details=""):
        record = {
            "Index": index,
            "Name": name,
            "Phone": phone,
            "Status": status,
            "Details": details,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.records.append(record)
        
        if status == "SUCCESS":
            logger.debug(f"Report: Contact {name} - Status: {status}")
        else:
            logger.warning(f"Report: Contact {name} - Status: {status} ({details})")

    def generate_report(self) -> str:
        if not self.records:
            logger.warning("No records to generate report.")
            return ""

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.output_dir, f"campaign_report_{timestamp}.csv")
        
        try:
            with open(report_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Index", "Name", "Phone", "Status", "Details", "Timestamp"])
                writer.writeheader()
                writer.writerows(self.records)
            
            logger.info(f"📊 Campaign execution report written to: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Failed to generate campaign report CSV file: {e}")
            return ""
