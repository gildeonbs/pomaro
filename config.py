import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "focus_time": 25,
    "short_break": 5,
    "long_break": 15,
    "sound_enabled": True
}

class ConfigManager:
    """Manages the application configurations, persisting them in a JSON file."""

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Loads configurations from disk or returns the default if it doesn't exist."""
        if not os.path.exists(CONFIG_FILE):
            ConfigManager.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensures that missing keys receive the default value
                for key, value in DEFAULT_CONFIG.items():
                    data.setdefault(key, value)
                return data
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()

    @staticmethod
    def save_config(config: Dict[str, Any]) -> None:
        """Saves the current configurations to disk."""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
