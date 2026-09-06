import json
from pathlib import Path

from .models import Transaction, Budget
from .exceptions import TransactionNotFoundError, DataStorageError
from .constants import DEFAULT_INCOME_CATEGORIES, DEFAULT_EXPENSE_CATEGORIES
from .logger import logger
from .storage import load_transactions, save_transactions, load_budgets, save_budgets

class ExpenseTracker:
    def __init__(self, data_file: str = "data.json", budget_file: str = "budgets.json"):
        self.transactions = []
        self.budgets = {}
        self.income_categories = list(DEFAULT_INCOME_CATEGORIES)
        self.expense_categories = list(DEFAULT_EXPENSE_CATEGORIES)
        self.data_file = Path(data_file)
        self.load_from_file()

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        logger.info(f"Додано нову транзакцію: {transaction}")
        self.save_to_file()

    def delete_transaction(self, index: int) -> Transaction:
        if 0 <= index < len(self.transactions):
            deleted = self.transactions.pop(index)
            logger.info(f"Видалено транзакцію під індексом {index + 1}: {deleted}")
            self.save_to_file()
            return deleted
        
        err_msg = f"Спроба видалення за некоректним індексом: {index + 1}"
        logger.warning(err_msg)
        raise TransactionNotFoundError(err_msg)

    def calculate_balance(self) -> float:
        return sum(tx.get_impact() for tx in self.transactions)

    def save_to_file(self):
        try:
            data = {
                "income_categories": self.income_categories,
                "expense_categories": self.expense_categories,
                "transactions": [tx.to_dict() for tx in self.transactions]
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info("Дані успішно збережено у JSON.")
        except Exception as e:
            logger.error(f"Помилка збереження у файл: {e}", exc_info=True)
            raise DataStorageError(f"Не вдалося зберегти дані: {e}")

    def load_from_file(self):
        if not self.data_file.exists():
            logger.warning(f"Файл {self.data_file} не знайдено. Створюємо нове сховище.")
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "income_categories" in data:
                self.income_categories = data["income_categories"]
            if "expense_categories" in data:
                self.expense_categories = data["expense_categories"]

            self.transactions.clear()
            for tx_data in data.get("transactions", []):
                self.transactions.append(Transaction.from_dict(tx_data))
                
            logger.info(f"Завантажено {len(self.transactions)} транзакцій з файлу.")
        except Exception as e:
            logger.error(f"Помилка зчитання JSON: {e}", exc_info=True)
            raise DataStorageError(f"Помилка завантаження даних: {e}")

    def set_budget(self, category: str, limit: float):
        budget = Budget(category, limit)
        self.budgets[category] = budget
        save_budgets(self.budget_file, self.budgets)
        logger.info(f"Встановлено бюджет для категорії '{category}': {limit} грн")

        