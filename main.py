from datetime import datetime

# Створюємо класи даних
class Transaction:
    def __init__(self, amount: float, category: str, description: str = ""):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def get_impact(self) -> float:
        return 0.0

    def __str__(self):
        return f"[{self.date}] {self.category}: {self.amount:.2f} грн ({self.description})"

class Income(Transaction):
    def get_impact(self) -> float:
        # Збільшує баланс
        return self.amount

    def __str__(self):
        return f"[ДОХІД] {super().__str__()}"


class Expense(Transaction):
    def __init__(self, amount: float, category: str, description: str = "", is_recurring: bool = False):
        super().__init__(amount, category, description)
        self.is_recurring = is_recurring

    def get_impact(self) -> float:
            # Зменьшує баланс
        return -self.amount

    def __str__(self):
        rec = "🔄" if self.is_recurring else ""
        return f"[ВИТРАТА] {super().__str__()}{rec}"


class Budget:
    def __init__(self, category: str, monthly_limit: float):
        self.category = category
        self.monthly_limit = monthly_limit

    def check_limit(self, current_expenses: float) ->str:
        if current_expenses > self.monthly_limit:
            over = current_expenses - self.monthly_limit
            return f"⚠️ Перевищено бюджет по '{self.category}' на {over:.2f} грн!"
        left = self.monthly_limit - current_expenses
        return f"✅ Бюджет '{self.category}': використано {current_expenses:.2f} з {self.monthly_limit:.2f} грн (Залишок: {left:.2f} грн)."


# Менеджер транзакцій

class ExpenseTracker:

    def __init__(self):
        self.transaction = []
        self.budgets = {}

    def add_transaction(self, transaction: Transaction):
        self.transaction.append(transaction)

    def delete_transaction(self, index: int) -> bool:
        if 0 <= index < len(self.transaction):
            deleted = self.transaction.pop(index)
            print(f"Видалено {deleted}")
            return True
        return False

    def set_budgets(self, category: str, limit: float):
        self.budgets[category] = Budget(category, limit)

    def calculate_balance(self) -> float:
        return sum(tx.get_impact() for tx in self.transaction)

    def get_category_expenses(self, category: str) -> float:
        return sum(tx.amount for tx in self.transaction if isinstance(tx, Expense) and tx.category.lower() == category.lower())

    def print_transactions(self):
        if not self.transaction:
            print("Список транзакцій порожній")
            return

        print("\n --- Список транзакцій ---")
        for i, tx in enumerate(self.transaction, 1):
            print(f"{i}. {tx}")

    def print_report(self):
        total_income = sum(tx.amount for tx in self.transaction if isinstance(tx, Income))
        total_expence = sum(tx.amount for tx in self.transaction if isinstance(tx, Expense))

        print("\n=== Звіт та баланс ===")
        print(f"Загальний дохід: +{total_income:.2f} грн")
        print(f"Загальні витрати: -{total_expence:.2f} грн")
        print(f"Поточний баланс: {self.calculate_balance():.2f} грн")
        print("=" *20)
