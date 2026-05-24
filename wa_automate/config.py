import os
import yaml

DEFAULT_CONFIG = {
    "campaign": {
        "input_file": "contacts1.xlsx",
        "default_message": "Hello {Name}, we are offering job opportunities under a CSR initiative. Reply if interested.",
        "dry_run": False,
        "default_country_code": "91"
    },
    "browser": {
        "headless": False,
        "maximize": True,
        "page_load_timeout": 30,
        "user_data_dir": "chrome-data"
    },
    "delays": {
        "min_delay": 15,
        "max_delay": 45,
        "batch_size": 10,
        "batch_cooldown": 300
    },
    "logging": {
        "level": "INFO",
        "log_file": "wa_automate.log",
        "log_to_console": True
    }
}

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.settings = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_settings = yaml.safe_load(f)
                    if user_settings:
                        self._deep_update(self.settings, user_settings)
            except Exception as e:
                print(f"Warning: Failed to load config file: {e}. Using defaults.")

    def _deep_update(self, base_dict, update_dict):
        for k, v in update_dict.items():
            if isinstance(v, dict) and k in base_dict and isinstance(base_dict[k], dict):
                self._deep_update(base_dict[k], v)
            else:
                base_dict[k] = v

    def get(self, *keys, default=None):
        val = self.settings
        for key in keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return default
        return val
