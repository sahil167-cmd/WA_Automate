import csv
import os
import datetime
from typing import List, Dict, Any
from .logger import logger

class CampaignReporter:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.records: List[Dict[str, Any]] = []
        os.makedirs(self.output_dir, exist_ok=True)

    def log_result(self, index: int, name: str, phone: str, status: str, details: str = "") -> None:
        record = {
            "Index": index,
            "Name": name,
            "Phone": phone,
            "Status": status,
            "Details": details,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.records.append(record)
        
        if status in ["SUCCESS", "DRY_RUN"]:
            logger.debug(f"Report: Contact {name} - Status: {status}")
        else:
            logger.warning(f"Report: Contact {name} - Status: {status} ({details})")

    def generate_report(self) -> str:
        """
        Generates a CSV report and a Markdown summary report.
        Returns the path of the generated CSV report.
        """
        if not self.records:
            logger.warning("No records to generate report.")
            return ""

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Generate CSV Report
        csv_path = os.path.join(self.output_dir, f"campaign_report_{timestamp}.csv")
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Index", "Name", "Phone", "Status", "Details", "Timestamp"])
                writer.writeheader()
                writer.writerows(self.records)
            logger.info(f"📊 Campaign CSV report written to: {csv_path}")
        except Exception as e:
            logger.error(f"Failed to generate campaign CSV report: {e}")
            csv_path = ""

        # 2. Generate Markdown Summary Report
        md_path = os.path.join(self.output_dir, f"campaign_report_{timestamp}.md")
        try:
            total = len(self.records)
            success = sum(1 for r in self.records if r["Status"] == "SUCCESS")
            dry_run = sum(1 for r in self.records if r["Status"] == "DRY_RUN")
            failed = sum(1 for r in self.records if r["Status"] == "FAILED")
            skipped = sum(1 for r in self.records if r["Status"] == "SKIPPED")
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# Campaign Execution Summary\n\n")
                f.write(f"- **Generated At**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"- **Total Contacts Processed**: {total}\n")
                f.write(f"- **Successful Sends**: {success}\n")
                f.write(f"- **Dry Run Mocked**: {dry_run}\n")
                f.write(f"- **Failed Sends**: {failed}\n")
                f.write(f"- **Skipped (Invalid Number)**: {skipped}\n\n")
                
                f.write("## Detailed Log\n\n")
                f.write("| Index | Name | Phone | Status | Details | Timestamp |\n")
                f.write("|-------|------|-------|--------|---------|-----------|\n")
                for r in self.records:
                    f.write(f"| {r['Index']} | {r['Name']} | {r['Phone']} | `{r['Status']}` | {r['Details']} | {r['Timestamp']} |\n")
            
            logger.info(f"📝 Campaign Markdown summary written to: {md_path}")
        except Exception as e:
            logger.error(f"Failed to generate campaign Markdown report: {e}")

        return csv_path
