import os
from typing import Dict, Any
from dataclasses import dataclass, field
import json

@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    db_name: str = "finance.db"

@dataclass
class UIConfig:
    """UI configuration settings."""
    theme: str = "dark"  # or "light"
    window_size: tuple = field(default_factory=lambda: (1024, 768))
    refresh_interval: int = 60  # seconds
    max_items_per_page: int = 50

@dataclass
class AppConfig:
    """Main application configuration."""
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    debug: bool = False
    log_level: str = "INFO"
    log_file: str = "app.log"

class ConfigManager:
    """Manages application configuration.
    
    Handles loading and saving configuration from/to files,
    and provides access to configuration settings.
    """
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize the configuration manager.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.config = AppConfig()
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file.
        
        If the file doesn't exist, creates it with default values.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.config = self._dict_to_config(data)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading config: {e}")
                self.save_config()  # Save default config if loading fails
        else:
            self.save_config()  # Create config file with defaults

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config_to_dict(self.config), f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def _config_to_dict(self, config: AppConfig) -> Dict[str, Any]:
        """Convert config object to dictionary.
        
        Args:
            config (AppConfig): Configuration object
            
        Returns:
            Dict[str, Any]: Dictionary representation of config
        """
        return {
            'database': {
                'db_name': config.database.db_name
            },
            'ui': {
                'theme': config.ui.theme,
                'window_size': config.ui.window_size,
                'refresh_interval': config.ui.refresh_interval,
                'max_items_per_page': config.ui.max_items_per_page
            },
            'debug': config.debug,
            'log_level': config.log_level,
            'log_file': config.log_file
        }

    def _dict_to_config(self, data: Dict[str, Any]) -> AppConfig:
        """Convert dictionary to config object.
        
        Args:
            data (Dict[str, Any]): Dictionary containing config data
            
        Returns:
            AppConfig: Configuration object
        """
        return AppConfig(
            database=DatabaseConfig(**data['database']),
            ui=UIConfig(**data['ui']),
            debug=data['debug'],
            log_level=data['log_level'],
            log_file=data['log_file']
        )

    def get_config(self) -> AppConfig:
        """Get current configuration.
        
        Returns:
            AppConfig: Current configuration object
        """
        return self.config

    def update_config(self, **kwargs) -> None:
        """Update configuration settings.
        
        Args:
            **kwargs: Configuration values to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            elif hasattr(self.config.database, key):
                setattr(self.config.database, key, value)
            elif hasattr(self.config.ui, key):
                setattr(self.config.ui, key, value)
        
        self.save_config() 