from datetime import datetime

from expense_tracker.tracker import ExpenseTracker


def seed(tracker: ExpenseTracker):
    tracker.add_transaction(15000.00, "income", "Salary", "Зарплата за січень")
    tracker.add_transaction(450.00, "expense", "Food", "Продукти на тиждень")
    tracker.add_transaction(120.00, "expense", "Transport", "Проїзний")
    tracker.add_transaction(2000.00, "income", "Freelance", "Підробіток")
    tracker.add_transaction(800.00, "expense", "Food", "Закупка на вихідні")
    tracker.add_transaction(300.00, "expense", "Entertainment", "Кіно з друзями")

    tracker.set_budget("Food", 1000.00)
    tracker.set_budget("Transport", 200.00)


def print_report(tracker: ExpenseTracker):
    print("=== Транзакції ===")
    for t in tracker.get_all_transactions():
        sign = "+" if t["transaction_type"] == "income" else "-"
        amount_str = f'{sign}{t["amount"]:.2f}'
        print(
            f'[{t["id"]}] {t["date"]} | {t["transaction_type"]:<7} | '
            f'{t["category"]:<10} | {amount_str:>9}'
        )

    print(f"\n=== Баланс: {tracker.calculate_balance():.2f} ===")

    print("\n=== Витрати за категоріями ===")
    for row in tracker.get_expenses_by_category():
        print(f'{row["category"]:<10} : {row["total"]:.2f}')


def demo_budget_check(tracker: ExpenseTracker):
    # check_budget_status дивиться на витрати ПОТОЧНОГО місяця, а тестові
    # дані вище без явної дати падають на сьогодні — тож спрацює одразу.
    tracker.add_transaction(1200.00, "expense", "Food", "Демо-витрата понад ліміт")

    print("\n=== Перевірка бюджетів (поточний місяць) ===")
    statuses = tracker.get_budget_status()
    if not any(s["exceeded"] for s in statuses):
        print("Усі категорії в межах ліміту.")


if __name__ == "__main__":
    tracker = ExpenseTracker(username="olexandr", email="olexandr@example.com")
    seed(tracker)
    print_report(tracker)
    demo_budget_check(tracker)
