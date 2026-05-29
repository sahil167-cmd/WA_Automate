# WA_Automate 🚀

`WA_Automate` is a robust, modular, production-grade command-line utility designed for automated, personalized message campaigns on WhatsApp Web using Selenium.

Built with safety, customizability, and logging at its core, this tool includes built-in anti-ban protection mechanisms, session persistence, media attachments, and detailed execution reports.

---

## Key Features 🌟

* 📂 **Multi-Source Input**: Supports importing contacts via Excel (`.xlsx`, `.xls`), CSV (`.csv`), and JSON (`.json`) files.
* ✍️ **Dynamic Templating**: Customize messages with placeholders (e.g., `{Name}`) and default fallbacks (e.g., `{Name|there}`) to handle missing values gracefully.
* 🛡️ **Anti-Ban Protections**:
  * **Jitter**: Randomized sleep intervals between messages mimicking natural human behavior.
  * **Batch Rate Limiting**: Automatic extended cooldown breaks after sending a specified batch of messages.
* 💾 **Session Persistence**: Saves Chrome browser user profile data locally, so you only scan the QR code once.
* 📎 **Media Attachments**: Support for sending photos, videos, and document files with automatic size validation (max 100MB).
* ℹ️ **Intelligent Dry-Run**: Simulate campaigns to preview exactly what messages will be sent, log validation issues, and estimate execution duration.
* 📊 **Campaign Reports**: Automatically generates timestamped CSV logs and Markdown summaries detailing success/failure rates and failure error reasons.
* ⏸️ **Interactive Pause/Resume**: Safely intercept running campaigns (`Ctrl+C`) to pause execution, resume later, or gracefully terminate and save progress.
* 🖥️ **Headless Browser Mode**: Option to run campaigns silently in the background with user-agent spoofing to avoid bot detection.
* 🧪 **Comprehensive Test Suite**: Automated unit tests for configuration, contact loaders, message templates, validation, and reporters.

---

## Project Structure 📁

```text
WA_Automate/
├── wa_automate/              # Core modular package
│   ├── __init__.py           # Package exports
│   ├── campaign.py           # Core campaign execution loop
│   ├── config.py             # Config file parser and settings validator
│   ├── data_loader.py        # CSV/Excel/JSON contact reader
│   ├── driver.py             # Selenium WebDriver controller
│   ├── exceptions.py         # Custom application-level exception classes
│   ├── logger.py             # Rotating file and console logger
│   ├── reporter.py           # Campaign CSV and Markdown reporter
│   ├── scheduler.py          # Anti-ban sleep/cooldown engine with metrics tracking
│   ├── templater.py          # Message placeholder interpolator with fallbacks
│   └── validator.py          # E.164 phone cleaner & validator
├── tests/                    # Unit test suite
│   ├── test_config.py
│   ├── test_data_loader.py
│   ├── test_reporter.py
│   ├── test_templater.py
│   └── test_validator.py
├── templates/                # Contact templates
│   ├── contacts_template.csv
│   └── contacts_template.xlsx
├── .github/
│   └── workflows/
│       └── python-app.yml    # GitHub Actions CI workflow
├── .gitignore
├── config.example.yaml       # Default configurations template
├── requirements.txt          # Third-party dependencies
├── requirements-dev.txt      # Testing and development dependencies
├── setup.py                  # Installation setup configuration
└── automate.py               # Main CLI wrapper entrypoint
```

---

## Installation & Setup 🛠️

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sahil167-cmd/WA_Automate.git
   cd WA_Automate
   ```

2. **Install Package**:
   Install the library locally in editable mode along with its dependencies:
   ```bash
   pip install -e .
   ```
   Or install development packages:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Configure Settings**:
   Copy the example settings template to create your active configuration:
   ```bash
   copy config.example.yaml config.yaml
   ```
   Open `config.yaml` to adjust campaign settings, timing parameters, and browser options.

---

## Command Line Interface (CLI) Usage 🚀

Start campaigns by executing `automate.py` or the registered console command `wa-automate`:

```bash
# Run campaign using active config.yaml settings
python automate.py

# Simulate execution (Dry-Run mode) to preview messages and estimate time
python automate.py --dry-run

# Run campaign using custom inputs and messages via CLI overrides
python automate.py -i templates/contacts_template.csv -m "Hey {Name|there}, checkout this opportunity!"

# Send an image or document along with your messages
python automate.py -i contacts.csv -a path/to/brochure.pdf

# Run browser execution in headless mode
python automate.py --headless

# Generate a sample CSV or Excel contact spreadsheet template
python automate.py --generate-template csv
python automate.py --generate-template xlsx
```

### CLI Parameters Reference:
* `-i`, `--input`: Custom path to contact spreadsheet (CSV/Excel/JSON).
* `-m`, `--message`: Custom message template. Supports fallback default formatting like `{Name|Customer}`.
* `-c`, `--config`: Path to custom YAML configuration file.
* `-d`, `--dry-run`: Runs campaign validations without launching Selenium or sending messages.
* `-a`, `--attachment`: Path to media file (image/document/video) to upload and send.
* `--headless`: Launches Chrome browser in headless mode.
* `--generate-template`: Generates dummy contact templates (`csv` or `xlsx`) in the `templates/` directory.

---

## Testing 🧪

Run the suite of automated tests using `pytest`:
```bash
python -m pytest
```

---


> WhatsApp strictly monitors automated sending. Exposing accounts to spam patterns will result in **permanent bans**.

To safeguard your WhatsApp account from being flagged or banned:
1. **Warm Up Accounts**: Avoid sending high-volume campaigns on newly registered SIM cards/accounts.
2. **Mimic Human Timings**: Ensure your configuration uses conservative delays. We recommend `min_delay: 20` and `max_delay: 60` with batch cooldowns.
3. **Use Personalization**: Personalizing message templates using placeholders and default fallbacks avoids sending identical copies of messages to multiple users.
4. **Acquire Consent**: Send campaigns only to users who have opted-in or expect communications from your organization.
