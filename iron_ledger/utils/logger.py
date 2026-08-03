import logging
import sys

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',      # Blue
        'INFO': '\033[92m',       # Green
        'WARNING': '\033[93m',    # Yellow
        'ERROR': '\033[91m',      # Red
        'CRITICAL': '\033[1;91m', # Bold Red
    }
    RESET = '\033[0m'
    CHECKMARK = '✓'

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        prefix = f"{color}{self.CHECKMARK} [{record.levelname}]{self.RESET}"
        record.msg = f"{prefix} {record.msg}"
        return super().format(record)

def setup_logger(name: str = "iron_ledger", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = ColoredFormatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
