from .tracker import ExpenseTracker
from .exceptions import InvalidAmountError, TransactionNotFoundError, DataStorageError
from .logger import logger


def print_menu():
    print("\n==============================")
    print("    EXPENSE TRACKER MENU      ")
    print("==============================")
    print("1. Додати дохід")
    print("2. Додати витрату")
    print("3. Переглянути всі транзакції")
    print("4. Переглянути баланс")
    print("5. Видалити транзакцію")
    print("6. Встановити бюджет для категорії")
    print("7. Переглянути бюджети")
    print("8. Перевірити стан бюджетів (поточний місяць)")
    print("0. Вихід")
    print("==============================")


def print_transaction(tx: dict):
    sign = "+" if tx["transaction_type"] == "income" else "-"
    emoji = "🟢" if tx["transaction_type"] == "income" else "🔴"
    desc = f" ({tx['description']})" if tx["description"] else ""
    print(f"[{tx['id']}] {tx['date']} {emoji} {tx['category']}: {sign}{tx['amount']:.2f} грн{desc}")


def run_cli():
    tracker = ExpenseTracker()

    while True:
        print_menu()
        choice = input("Оберіть дію: ").strip()

        try:
            if choice == "1":
                amount = float(input("Введіть суму доходу: "))
                category = input("Введіть категорію: ").strip() or "Дохід"
                description = input("Введіть опис (необов'язково): ").strip()

                tracker.add_transaction(amount, "income", category, description)
                print("✅ Дохід успішно додано!")

            elif choice == "2":
                amount = float(input("Введіть суму витрати: "))
                category = input("Введіть категорію: ").strip() or "Витрата"
                description = input("Введіть опис (необов'язково): ").strip()
                is_recurring = input("Регулярна витрата? (так/ні): ").strip().lower() in ["так", "yes", "y", "1"]
                if is_recurring:
                    description = f"{description} 🔄 [регулярна]".strip()

                tracker.add_transaction(amount, "expense", category, description)
                print("✅ Витрату успішно додано!")

            elif choice == "3":
                transactions = tracker.get_all_transactions()
                if not transactions:
                    print("\nℹ️ Список транзакцій порожній.")
                else:
                    print("\n--- СПИСОК УСІХ ТРАНЗАКЦІЙ ---")
                    for tx in transactions:
                        print_transaction(tx)
                    print("-------------------------------")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "4":
                balance = tracker.calculate_balance()
                print("\n--- БАЛАНС ТА ЗВІТ ---")
                print(f"Поточний баланс: {balance:.2f} грн")
                print("----------------------")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "5":
                transactions = tracker.get_all_transactions()
                if not transactions:
                    print("\nℹ️ Немає транзакцій для видалення.")
                    input("\nНатисніть Enter, щоб повернутися в меню...")
                    continue

                print("\n--- СПИСОК ТРАНЗАКЦІЙ ---")
                for tx in transactions:
                    print_transaction(tx)
                print("-------------------------")

                transaction_id = int(input("Введіть номер [id] транзакції для видалення: "))
                tracker.delete_transaction(transaction_id)
                print(f"✅ Транзакцію id={transaction_id} успішно видалено!")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "6":
                category = input("Введіть категорію: ").strip()
                limit = float(input("Введіть ліміт бюджету: "))
                tracker.set_budget(category, limit)
                print("✅ Бюджет успішно встановлено!")

            elif choice == "7":
                budgets = tracker.get_budgets()
                if not budgets:
                    print("\nℹ️ Бюджети ще не встановлено.")
                else:
                    print("\n--- БЮДЖЕТИ ---")
                    for b in budgets:
                        print(f"🎯 Бюджет [{b['category']}]: {b['monthly_limit']:.2f} грн")
                    print("---------------")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "8":
                statuses = tracker.get_budget_status()
                if not statuses:
                    print("\nℹ️ Бюджети ще не встановлено.")
                else:
                    print("\n--- СТАН БЮДЖЕТІВ (поточний місяць) ---")
                    for s in statuses:
                        mark = "⚠️ " if s["exceeded"] else "✅ "
                        print(f"{mark}{s['category']:<12}: {s['spent']:.2f} / {s['monthly_limit']:.2f} грн")
                    print("----------------------------------------")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "0":
                print("\nДякуємо за використання Expense Tracker! До побачення 👋")
                logger.info("Завершення роботи CLI.")
                break

            else:
                print("\n⚠️ Некоректний вибір. Спробуйте ще раз.")

        except ValueError as e:
            print(f"\n⚠️ Некоректне значення: {e}. Будь ласка, введіть числові дані там, де це потрібно.")
            logger.warning(f"Помилка введення користувача: {e}")
            input("\nНатисніть Enter, щоб продовжити...")

        except (InvalidAmountError, TransactionNotFoundError) as e:
            print(f"\n⚠️ Помилка: {e}")
            input("\nНатисніть Enter, щоб продовжити...")

        except DataStorageError as e:
            print(f"\n❌ Помилка бази даних: {e}")
            input("\nНатисніть Enter, щоб продовжити...")

        except Exception as e:
            print(f"\n💥 Несподівана помилка: {e}")
            logger.critical(f"Неперехоплений виняток у CLI: {e}", exc_info=True)
            input("\nНатисніть Enter, щоб продовжити...")
