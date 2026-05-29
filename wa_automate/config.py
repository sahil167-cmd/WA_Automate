import os
import yaml
from typing import Any, Tuple
from .exceptions import ConfigError

DEFAULT_CONFIG = {
    "campaign": {
        "input_file": "contacts1.xlsx",
        "default_message": "Hello {Name}, we are offering job opportunities under a CSR initiative. Reply if interested.",
        "dry_run": False,
        "default_country_code": "91",
        "attachment": None
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
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.settings = DEFAULT_CONFIG.copy()
        self.load()
        self.validate()

    def load(self) -> None:
        """Loads configuration from YAML file, merging with default settings."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_settings = yaml.safe_load(f)
                    if user_settings:
                        if not isinstance(user_settings, dict):
                            raise ConfigError("Configuration file must contain a key-value mapping.")
                        self._deep_update(self.settings, user_settings)
            except Exception as e:
                raise ConfigError(f"Failed to load config file '{self.config_path}': {e}") from e

    def _deep_update(self, base_dict: dict, update_dict: dict) -> None:
        """Recursively updates a nested dictionary."""
        for k, v in update_dict.items():
            if isinstance(v, dict) and k in base_dict and isinstance(base_dict[k], dict):
                self._deep_update(base_dict[k], v)
            else:
                base_dict[k] = v

    def get(self, *keys: str, default: Any = None) -> Any:
        """Retrieves a nested configuration value using path keys."""
        val = self.settings
        for key in keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return default
        return val

    def validate(self) -> None:
        """Validates that keys have proper types and settings are valid."""
        # Validate delays
        min_delay = self.get("delays", "min_delay")
        max_delay = self.get("delays", "max_delay")
        
        if not isinstance(min_delay, (int, float)) or not isinstance(max_delay, (int, float)):
            raise ConfigError("Delays min_delay and max_delay must be numbers.")
        
        if min_delay < 0 or max_delay < 0:
            raise ConfigError("Delay settings cannot be negative.")
            
        if min_delay > max_delay:
            raise ConfigError("min_delay cannot be greater than max_delay.")

        # Validate batch configuration
        batch_size = self.get("delays", "batch_size")
        batch_cooldown = self.get("delays", "batch_cooldown")
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ConfigError("batch_size must be a positive integer.")
        if not isinstance(batch_cooldown, (int, float)) or batch_cooldown < 0:
            raise ConfigError("batch_cooldown must be a non-negative number.")
