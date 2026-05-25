# WA_Automate 🚀

`WA_Automate` is a robust, modular, production-grade command-line utility designed for automated, personalized message campaigns on WhatsApp Web using Selenium.

Built with safety, customizability, and logging at its core, this tool includes built-in anti-ban protection mechanisms, session persistence, media attachments, and detailed execution reports.

---

## Key Features 🌟

* 📂 **Multi-Source Input**: Supports importing contacts via both Excel (`.xlsx`, `.xls`) and CSV files.
* ✍️ **Dynamic Templating**: Customize messages with placeholders (e.g. `{Name}`) that automatically bind to columns in your contact list.
* 🛡️ **Anti-Ban Protections**:
  * **Jitter**: Randomized sleep intervals between messages mimicking natural human behavior.
  * **Batch Rate Limiting**: Automatic extended cooldown breaks after sending a specified batch of messages.
* 💾 **Session Persistence**: Saves Chrome browser user profile data locally, so you only scan the QR code once.
* 📎 **Media Attachments**: Support for sending photos, videos, and document files along with text messages.
* ℹ️ **Intelligent Dry-Run**: Simulate campaigns to preview exactly what messages will be sent, log validation issues, and estimate execution duration without spawning browsers or sending messages.
* 📊 **Campaign Reports**: Automatically generates timestamped CSV logs detailing success/failure rates and failure error reasons for auditing.
* ⏸️ **Interactive Pause/Resume**: Safely intercept running campaigns (`Ctrl+C`) to pause execution, resume later, or gracefully terminate and save progress.
* 🖥️ **Headless Browser Mode**: Option to run campaigns silently in the background with user-agent spoofing to avoid bot detection.

---

## Project Structure 📁

```text
WA_Automate/
├── wa_automate/              # Core modular package
│   ├── __init__.py
│   ├── campaign.py           # Core campaign execution loop
│   ├── config.py             # Config file parser
│   ├── data_loader.py        # CSV/Excel reader
│   ├── driver.py             # Selenium WebDriver controller
│   ├── logger.py             # Structured dual-output logger
│   ├── reporter.py           # Campaign CSV reporter
│   ├── scheduler.py          # Anti-ban sleep/cooldown engine
│   ├── templater.py          # Message placeholder interpolator
│   └── validator.py          # E.164 phone cleaner & validator
├── templates/                # Contact templates
│   ├── contacts_template.csv
│   └── contacts_template.xlsx
├── .gitignore
├── config.example.yaml       # Default configurations template
├── requirements.txt          # Third-party dependencies
└── automate.py               # Main CLI wrapper entrypoint
```

---

## Installation & Setup 🛠️

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sahil167-cmd/WA_Automate.git
   cd WA_Automate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**:
   Copy the example settings template to create your active configuration:
   ```bash
   copy config.example.yaml config.yaml
   ```
   Open `config.yaml` to adjust campaign settings, timing parameters, and browser options.

---

## Command Line Interface (CLI) Usage 🚀

Start campaigns by executing `automate.py`:

```bash
# Run campaign using active config.yaml settings
python automate.py

# Simulate execution (Dry-Run mode) to preview messages and estimate time
python automate.py --dry-run

# Run campaign using custom inputs and messages via CLI overrides
python automate.py -i templates/contacts_template.csv -m "Hey {Name}, checkout this opportunity!"

# Send an image or document along with your messages
python automate.py -i contacts.csv -a path/to/brochure.pdf

# Run browser execution in headless mode
python automate.py --headless
```

### CLI Parameters Reference:
* `-i`, `--input`: Custom path to contact spreadsheet (CSV/Excel).
* `-m`, `--message`: Custom message template.
* `-c`, `--config`: Path to custom YAML configuration file.
* `-d`, `--dry-run`: Runs campaign validations without launching Selenium or sending messages.
* `-a`, `--attachment`: Path to media file (image/document/video) to upload and send.
* `--headless`: Launches Chrome browser in headless mode.

---


> WhatsApp strictly monitors automated sending. Exposing accounts to spam patterns will result in **permanent bans**.

To safeguard your WhatsApp account from being flagged or banned:
1. **Warm Up Accounts**: Avoid sending high-volume campaigns on newly registered SIM cards/accounts.
2. **Mimic Human Timings**: Ensure your configuration uses conservative delays. We recommend `min_delay: 20` and `max_delay: 60` with batch cooldowns.
3. **Use Personalization**: Personalizing message templates using the `{Name}` placeholder avoids sending identical copies of messages to multiple users.
4. **Acquire Consent**: Send campaigns only to users who have opted-in or expect communications from your organization.
