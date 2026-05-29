import os
import pytest
import yaml
from wa_automate.config import Config
from wa_automate.exceptions import ConfigError

@pytest.fixture
def temp_config_yaml():
    path = os.path.join(os.path.dirname(__file__), "temp_config.yaml")
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_default_config():
    # If file doesn't exist, it should use default configurations
    config = Config("non_existent_config.yaml")
    assert config.get("campaign", "default_country_code") == "91"
    assert config.get("delays", "min_delay") == 15
    assert config.get("delays", "max_delay") == 45

def test_custom_config_override(temp_config_yaml):
    custom_data = {
        "campaign": {
            "default_country_code": "1",
            "dry_run": True
        },
        "delays": {
            "min_delay": 5,
            "max_delay": 10
        }
    }
    with open(temp_config_yaml, "w") as f:
        yaml.dump(custom_data, f)

    config = Config(temp_config_yaml)
    assert config.get("campaign", "default_country_code") == "1"
    assert config.get("campaign", "dry_run") is True
    assert config.get("delays", "min_delay") == 5
    assert config.get("delays", "max_delay") == 10
    # Checks default values are preserved
    assert config.get("browser", "maximize") is True

def test_invalid_delays_validation(temp_config_yaml):
    # min_delay > max_delay should raise ConfigError
    bad_data = {
        "delays": {
            "min_delay": 50,
            "max_delay": 10
        }
    }
    with open(temp_config_yaml, "w") as f:
        yaml.dump(bad_data, f)

    with pytest.raises(ConfigError) as excinfo:
        Config(temp_config_yaml)
    assert "min_delay cannot be greater than max_delay" in str(excinfo.value)
