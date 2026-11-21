import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Створюємо папку для логів, якщо її немає
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

file_handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=1_000_000,   # ~1 МБ
    backupCount=3,
    encoding="utf-8"
)

# Налаштовуємо конфігурацію логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        file_handler,
        logging.StreamHandler() # Вивід у консоль (за бажанням)
    ]
)

logger = logging.getLogger("ExpenseTracker")