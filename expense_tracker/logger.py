import logging
from pathlib import Path

# Створюємо папку для логів, якщо її немає
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Налаштовуємо конфігурацію логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8"), # Запис у файл
        logging.StreamHandler() # Вивід у консоль (за бажанням)
    ]
)

logger = logging.getLogger("ExpenseTracker")