from pathlib import Path

from .models import Transaction, Budget
from .exceptions import TransactionNotFoundError
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
        self.budget_file = Path(budget_file)
        self.load_from_file()
        self.budgets = load_budgets(self.budget_file)

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
        save_transactions(self.data_file, self.transactions, self.income_categories, self.expense_categories)
        logger.info("Дані успішно збережено у JSON.")

    def load_from_file(self):
        self.transactions, inc_cats, exp_cats = load_transactions(self.data_file)
        if inc_cats:
            self.income_categories = inc_cats
        if exp_cats:
            self.expense_categories = exp_cats
        logger.info(f"Завантажено {len(self.transactions)} транзакцій з файлу.")

    def set_budget(self, category: str, limit: float):
        budget = Budget(category, limit)
        if category in self.budgets:
            logger.warning(f"Бюджет для категорії '{category}' вже існує, оновлюємо ліміт.")
        self.budgets[category] = budget
        save_budgets(self.budget_file, self.budgets)
        logger.info(f"Встановлено бюджет для категорії '{category}': {limit} грн")