from datetime import datetime
from .exceptions import InvalidAmountError

class Transaction:
    def __init__(self, amount: float, category: str, description: str = "", date_str: str = None):
        if amount <= 0:
            raise InvalidAmountError("Сума повинна бути більшою за 0!")
            
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date_str or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_impact(self) -> float:
        raise NotImplementedError("Метод повинен бути реалізований у дочірньому класі")

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: dict):
        t_type = data.get("type")
        if t_type == "Income":
            return Income(
                amount=data["amount"],
                category=data["category"],
                description=data.get("description", ""),
                date_str=data.get("date")
            )
        elif t_type == "Expense":
            return Expense(
                amount=data["amount"],
                category=data["category"],
                description=data.get("description", ""),
                is_recurring=data.get("is_recurring", False),
                date_str=data.get("date")
            )
        raise ValueError("Невідомий тип транзакції")


class Income(Transaction):
    def get_impact(self) -> float:
        return self.amount

    def __str__(self):
        return f"[{self.date}] 🟢 Дохід: {self.amount:.2f} грн | {self.category} ({self.description})"


class Expense(Transaction):
    def __init__(self, amount: float, category: str, description: str = "", is_recurring: bool = False, date_str: str = None):
        super().__init__(amount, category, description, date_str)
        self.is_recurring = is_recurring

    def get_impact(self) -> float:
        return -self.amount

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["is_recurring"] = self.is_recurring
        return data

    def __str__(self):
        rec_symbol = " 🔄" if self.is_recurring else ""
        return f"[{self.date}] 🔴 Витрата: {self.amount:.2f} грн | {self.category} ({self.description}){rec_symbol}"