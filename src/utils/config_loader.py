import os
from typing import Any, Dict, Optional

import yaml


class ConfigLoader:
    """
    A utility class for loading configuration from YAML or JSON files.
    Handles missing files and provides default configurations.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ConfigLoader.

        Args:
            config_path: Path to the configuration file. If None, uses default path.
        """
        self.config_path = config_path or self._get_default_config_path()

    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        return os.path.join(
            os.path.dirname(__file__), "..", "..", "config", "config.yaml"
        )

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the specified file.

        Returns:
            Dictionary containing the configuration data.

        Raises:
            FileNotFoundError: If the config file is not found.
            yaml.YAMLError: If there's an error parsing the YAML file.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                return config or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {self.config_path}: {e}")

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value.

        Args:
            key: The configuration key (dot-separated for nested keys).
            default: Default value if key is not found.

        Returns:
            The configuration value or default.
        """
        config = self.load_config()
        keys = key.split(".")
        value = config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to the file.

        Args:
            config: Configuration dictionary to save.
        """
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            raise Exception(f"Error saving config to {self.config_path}: {e}")


# Global instance for easy access
config_loader = ConfigLoader()
