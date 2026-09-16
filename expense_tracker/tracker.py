from . import models
from .database import get_connection, init_db
from .exceptions import TransactionNotFoundError
from .logger import logger


class ExpenseTracker:
    def __init__(self, username: str = "local_user", email: str = "local_user@example.com"):
        init_db()
        self.username = username
        self.user_id = self._get_or_create_user(username, email)
        logger.info(f"Трекер ініціалізовано для користувача '{username}' (id={self.user_id}).")

    @staticmethod
    def _get_or_create_user(username: str, email: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return row["id"]
        return models.create_user(username, email)

    def add_transaction(self, amount: float, transaction_type: str, category: str, description: str = "") -> int:
        return models.add_transaction(self.user_id, amount, transaction_type, category, description)

    def delete_transaction(self, transaction_id: int) -> int:
        deleted = models.delete_transaction(transaction_id)
        if not deleted:
            err_msg = f"Транзакцію з id={transaction_id} не знайдено."
            logger.warning(err_msg)
            raise TransactionNotFoundError(err_msg)
        return transaction_id

    def get_all_transactions(self) -> list:
        return models.get_all_transactions(self.user_id)

    def calculate_balance(self) -> float:
        return models.get_balance(self.user_id)

    def get_expenses_by_category(self) -> list:
        return models.get_expenses_by_category(self.user_id)

    def set_budget(self, category: str, limit: float):
        return models.set_budget(self.user_id, category, limit)

    def get_budgets(self) -> list:
        return models.get_budgets(self.user_id)

    def get_budget_status(self) -> list:
        return models.check_budget_status(self.user_id)