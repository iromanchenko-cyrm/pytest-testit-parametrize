"""Work with logging"""

from logging import DEBUG, Formatter, StreamHandler, basicConfig, getLogger
from sys import stdout

from pytest_testit_parametrize.constants import PLUGIN_NAME


class Logger:
    """Logger class"""

    def __init__(
        self, logger_name: str, logger_base_name: str = PLUGIN_NAME, level: int = DEBUG
    ):
        console_handler = StreamHandler(stdout)
        console_handler.setLevel(DEBUG)

        formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        console_handler.setFormatter(formatter)

        basicConfig(
            encoding="utf-8",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[console_handler],
        )
        self.logger = getLogger(f"{logger_base_name}.{logger_name}")
        self.set_level(level)

    def get_logger(self):
        """Get logger"""
        return self.logger

    def set_level(self, level=DEBUG):
        """Set level"""
        self.logger.setLevel(level)
