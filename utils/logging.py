import logging
import logging.handlers
import os
from typing import Optional
from config.settings import ConfigManager

def setup_logging(config: Optional[ConfigManager] = None) -> None:
    """Set up logging configuration.
    
    Configures logging with both file and console handlers,
    using settings from the config manager if provided.
    
    Args:
        config (Optional[ConfigManager]): Configuration manager instance
    """
    if config is None:
        config = ConfigManager()

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.get_config().log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(config.get_config().log_level)

    # Clear existing handlers
    root_logger.handlers = []

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        config.get_config().log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.
    
    Args:
        name (str): Name of the module/component
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)

class LoggingContext:
    """Context manager for temporary logging configuration.
    
    Allows temporarily changing logging configuration within a context.
    Useful for temporarily increasing log level for specific operations.
    """
    
    def __init__(self, level: int):
        """Initialize the logging context.
        
        Args:
            level (int): Logging level to set temporarily
        """
        self.level = level
        self.previous_level = None

    def __enter__(self):
        """Enter the context, saving current level and setting new one."""
        root_logger = logging.getLogger()
        self.previous_level = root_logger.level
        root_logger.setLevel(self.level)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context, restoring previous logging level."""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.previous_level) 