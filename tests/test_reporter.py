import os
import shutil
import pytest
from wa_automate.reporter import CampaignReporter

@pytest.fixture
def temp_report_dir():
    dir_name = "test_reports"
    yield dir_name
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

def test_reporter_generation(temp_report_dir):
    reporter = CampaignReporter(output_dir=temp_report_dir)
    
    # Verify records list is initially empty
    assert len(reporter.records) == 0
    
    # Log some dummy results
    reporter.log_result(1, "Alice", "919999999999", "SUCCESS")
    reporter.log_result(2, "Bob", "123", "SKIPPED", "Invalid phone number")
    reporter.log_result(3, "Charlie", "918888888888", "FAILED", "Timeout waiting for element")
    
    assert len(reporter.records) == 3
    
    # Generate reports
    csv_path = reporter.generate_report()
    
    # Assert CSV file exists
    assert os.path.exists(csv_path)
    
    # Assert MD file also exists in the same folder
    md_filename = os.path.basename(csv_path).replace(".csv", ".md")
    md_path = os.path.join(temp_report_dir, md_filename)
    assert os.path.exists(md_path)
    
    # Check that contents contain our strings
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        assert "Alice" in md_content
        assert "SUCCESS" in md_content
        assert "Bob" in md_content
        assert "SKIPPED" in md_content
        assert "Charlie" in md_content
        assert "FAILED" in md_content
        assert "Timeout waiting for element" in md_content
