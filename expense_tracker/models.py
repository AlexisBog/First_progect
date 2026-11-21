import sqlite3
from datetime import datetime

from .database import get_connection
from .exceptions import InvalidAmountError, DataStorageError
from .logger import logger


def create_user(username: str, email: str) -> int:
    """Створює користувача і повертає його id."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email),
        )
        conn.commit()
        user_id = cursor.lastrowid
        logger.info(f"Створено користувача '{username}' (id={user_id}).")
        return user_id
    except sqlite3.IntegrityError as e:
        logger.warning(f"Не вдалося створити користувача '{username}': {e}")
        raise DataStorageError(f"Користувач з таким username/email вже існує: {e}")
    finally:
        conn.close()


def add_transaction(
    user_id: int,
    amount: float,
    transaction_type: str,
    category: str,
    description: str = "",
    date: str = None,
) -> int:
    """Додає транзакцію (дохід або витрату) і повертає її id."""
    if amount <= 0:
        raise InvalidAmountError("Сума повинна бути більшою за 0!")
    if transaction_type not in ("income", "expense"):
        raise ValueError("transaction_type має бути 'income' або 'expense'")

    date = date or datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (amount, transaction_type, category, date, description, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (amount, transaction_type, category, date, description, user_id),
        )
        conn.commit()
        transaction_id = cursor.lastrowid
        logger.info(
            f"Додано транзакцію id={transaction_id} ({transaction_type}, "
            f"{amount:.2f}, {category}) для user_id={user_id}."
        )
        return transaction_id
    finally:
        conn.close()


def get_all_transactions(user_id: int) -> list:
    """Повертає всі транзакції конкретного користувача, відсортовані за датою."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, amount, transaction_type, category, date, description
            FROM transactions
            WHERE user_id = ?
            ORDER BY date, id
            """,
            (user_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_balance(user_id: int) -> float:
    """Повертає різницю між доходами та витратами користувача."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) AS total_income,
                SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) AS total_expense
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        total_income = row["total_income"] or 0.0
        total_expense = row["total_expense"] or 0.0
        return round(total_income - total_expense, 2)
    finally:
        conn.close()


def get_expenses_by_category(user_id: int) -> list:
    """Повертає витрати користувача, згруповані за категорією."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM transactions
            WHERE user_id = ? AND transaction_type = 'expense'
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id,),
        )
        return [{"category": r["category"], "total": r["total"]} for r in cursor.fetchall()]
    finally:
        conn.close()


def set_budget(user_id: int, category: str, monthly_limit: float) -> int:
    """Встановлює місячний бюджет для категорії і повертає id запису.

    Якщо бюджет для цієї категорії вже є — оновлює ліміт замість дубля.
    """
    if monthly_limit <= 0:
        raise InvalidAmountError("Ліміт бюджету повинен бути більшим за 0!")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM budgets WHERE user_id = ? AND category = ?",
            (user_id, category),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE budgets SET monthly_limit = ? WHERE id = ?",
                (monthly_limit, existing["id"]),
            )
            conn.commit()
            logger.warning(f"Бюджет для категорії '{category}' вже існує, оновлюємо ліміт.")
            return existing["id"]

        cursor.execute(
            "INSERT INTO budgets (category, monthly_limit, user_id) VALUES (?, ?, ?)",
            (category, monthly_limit, user_id),
        )
        conn.commit()
        budget_id = cursor.lastrowid
        logger.info(f"Встановлено бюджет для категорії '{category}': {monthly_limit:.2f} грн.")
        return budget_id
    finally:
        conn.close()


def get_budgets(user_id: int) -> list:
    """Допоміжна функція: повертає всі бюджети користувача для CLI-меню."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT category, monthly_limit FROM budgets WHERE user_id = ?",
            (user_id,),
        )
        return [{"category": r["category"], "monthly_limit": r["monthly_limit"]} for r in cursor.fetchall()]
    finally:
        conn.close()


def delete_transaction(transaction_id: int) -> bool:
    """Видаляє транзакцію за id. Повертає True, якщо запис був видалений."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"Видалено транзакцію id={transaction_id}.")
        else:
            logger.warning(f"Спроба видалення неіснуючої транзакції id={transaction_id}.")
        return deleted
    finally:
        conn.close()


def check_budget_status(user_id: int) -> list:
    """
    Бонус: порівнює фактичні витрати поточного місяця за кожною категорією
    з встановленим бюджетом. Повертає список статусів і друкує попередження,
    якщо ліміт перевищено.
    """
    current_month = datetime.now().strftime("%Y-%m")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                b.category AS category,
                b.monthly_limit AS monthly_limit,
                COALESCE(SUM(t.amount), 0) AS spent
            FROM budgets b
            LEFT JOIN transactions t
                ON t.category = b.category
                AND t.user_id = b.user_id
                AND t.transaction_type = 'expense'
                AND strftime('%Y-%m', t.date) = ?
            WHERE b.user_id = ?
            GROUP BY b.category, b.monthly_limit
            """,
            (current_month, user_id),
        )
        rows = cursor.fetchall()
    finally:
        conn.close()

    statuses = []
    for row in rows:
        spent = row["spent"] or 0.0
        limit = row["monthly_limit"]
        exceeded = spent > limit
        statuses.append({
            "category": row["category"],
            "monthly_limit": limit,
            "spent": round(spent, 2),
            "exceeded": exceeded,
        })
        if exceeded:
            msg = f"Перевищено бюджет для '{row['category']}': витрачено {spent:.2f} з {limit:.2f}"
            print(f"⚠️  {msg}")
            logger.warning(msg)

    return statuses