"""
Декоратори для ExpenseTracker: логування фінансових операцій,
валідація суми та заглушка під майбутню конвертацію валют (Заняття 25).

Примітка: замість окремого logging.basicConfig() з умови файл використовує
вже наявний logger проєкту (expense_tracker/logger.py, пише в logs/app.log),
щоб не плодити другий, конкуруючий конфіг логування.
"""

import functools
import inspect

from datetime import datetime

from .logger import logger

# Людські підписи для аргументів у логах (amount -> сума, category -> категорія тощо)
_LABELS = {
    "amount": "сума",
    "category": "категорія",
    "transaction_type": "тип",
    "description": "опис",
    "transaction_id": "id",
}


def _format_args(func, args, kwargs) -> str:
    """Формує рядок виду 'сума=350, категорія='food'' з реальних аргументів виклику."""
    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    parts = []
    for name, value in bound.arguments.items():
        if name == "self":
            continue
        label = _LABELS.get(name, name)
        parts.append(f"{label}={value!r}")
    return ", ".join(parts)


def log_transaction(func):
    """
    Логує кожну фінансову операцію — тип, суму, категорію, час.
    Рівень логування — INFO.
    Використовується на: add_income, add_expense, delete_transaction
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_time = datetime.now().strftime("%H:%M:%S")
        result = func(*args, **kwargs)
        arg_str = _format_args(func, args, kwargs)
        logger.info(f"{func.__name__}: {arg_str}, час={call_time}")
        return result
    return wrapper


def validate_amount(func):
    """
    Перевіряє перший числовий аргумент (amount):
    — має бути int або float
    — має бути > 0
    Якщо ні — логує WARNING і повертає None.
    Використовується на: add_income, add_expense
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        amount = bound.arguments.get("amount")

        is_valid_number = isinstance(amount, (int, float)) and not isinstance(amount, bool)
        if not is_valid_number or amount <= 0:
            logger.warning(f"{func.__name__}: сума має бути > 0, отримано: {amount!r}")
            return None

        return func(*args, **kwargs)
    return wrapper


def currency_aware(base_currency: str = "UAH"):
    """
    ЗАГЛУШКА — буде реалізовано у Занятті 25 (HTTP + requests).
    Майбутня логіка:
    — отримати поточний курс валюти через API
    — якщо транзакція в іноземній валюті — конвертувати в base_currency
    — зберегти обидва значення (оригінальне і конвертоване)
    Зараз: просто викликає функцію без змін і логує DEBUG повідомлення.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(
                f"[currency_aware] Конвертація ще не реалізована. "
                f"Базова валюта: {base_currency}"
            )
            # TODO (Заняття 25): отримати курс через requests.get(EXCHANGE_API_URL)
            # TODO (Заняття 25): конвертувати суму якщо currency != base_currency
            return func(*args, **kwargs)
        return wrapper
    return decorator
