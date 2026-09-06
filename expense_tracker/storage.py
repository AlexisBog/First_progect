import json
from pathlib import Path
from .models import Transaction, Budget
from .logger import logger
from .exceptions import DataStorageError


def load_transactions(file_path: Path) -> list:
    if not file_path.exists():
        return [], [], []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            txs = [Transaction.from_dict(tx) for tx in data.get("transactions", [])]
            inc_cats = data.get("income_categories", [])
            exp_cats = data.get("expense_categories", [])
            return txs, inc_cats, exp_cats
    except Exception as e:
        logger.error(f"Помилка завантаження транзакцій: {e}", exc_info=True)
        raise DataStorageError(f"Не вдалося зчитати транзакції: {e}")


def save_transactions(file_path: Path, transactions: list, income_cats: list = None, expense_cats: list = None):
    try:
        data = {
            "income_categories": income_cats or [],
            "expense_categories": expense_cats or [],
            "transactions": [tx.to_dict() for tx in transactions]
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Помилка збереження транзакцій: {e}", exc_info=True)
        raise DataStorageError(f"Не вдалося зберегти транзакції: {e}")
#def save_transactions(file_path: Path, transactions: list):
#    try:
#        data = {"transactions": [tx.to_dict() for tx in transactions]}
#        with open(file_path, "w", encoding="utf-8") as f:
#            json.dump(data, f, ensure_ascii=False, indent=4)
#    except Exception as e:
#        logger.error(f"Помилка збереження транзакцій: {e}", exc_info=True)
#        raise DataStorageError(f"Не вдалося зберегти транзакції: {e}")


def load_budgets(file_path: Path) -> dict:
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {b["category"]: Budget.from_dict(b) for b in data.get("budgets", [])}
    except Exception as e:
        logger.error(f"Помилка завантаження бюджетів: {e}", exc_info=True)
        raise DataStorageError(f"Не вдалося зчитати бюджети: {e}")


def save_budgets(file_path: Path, budgets: dict):
    try:
        data = {"budgets": [b.to_dict() for b in budgets.values()]}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Помилка збереження бюджетів: {e}", exc_info=True)
        raise DataStorageError(f"Не вдалося зберегти бюджети: {e}")