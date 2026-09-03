from .tracker import ExpenseTracker
from .models import Income, Expense
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
    print("0. Вихід")
    print("==============================")

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
                
                income = Income(amount, category, description)
                tracker.add_transaction(income)
                tracker.save_to_file()
                print("✅ Дохід успішно додано!")

            elif choice == "2":
                amount = float(input("Введіть суму витрати: "))
                category = input("Введіть категорію: ").strip() or "Витрата"
                description = input("Введіть опис (необов'язково): ").strip()
                is_recurring = input("Регулярна витрата? (так/ні): ").strip().lower() in ["так", "yes", "y", "1"]

                expense = Expense(amount, category, description, is_recurring=is_recurring)
                tracker.add_transaction(expense)
                tracker.save_to_file()
                print("✅ Витрату успішно додано!")

            elif choice == "3":
                if not tracker.transactions:
                    print("\nℹ️ Список транзакцій порожній.")
                else:
                    print("\n--- СПИСОК УСІХ ТРАНЗАКЦІЙ ---")
                    for i, tx in enumerate(tracker.transactions, 1):
                        print(f"{i}. {tx}")
                    print("-------------------------------")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "4":
                balance = tracker.calculate_balance()
                print("\n--- БАЛАНС ТА ЗВІТ ---")
                print(f"Поточний баланс: {balance:.2f} грн")
                print("----------------------")
                input("\nНатисніть Enter, щоб повернутися в меню...")

            elif choice == "5":
                if not tracker.transactions:
                    print("\nℹ️ Немає транзакцій для видалення.")
                    input("\nНатисніть Enter, щоб повернутися в меню...")
                    continue

                print("\n--- СПИСОК ТРАНЗАКЦІЙ ---")
                for i, tx in enumerate(tracker.transactions, 1):
                    print(f"{i}. {tx}")
                print("-------------------------")

                index = int(input("Введіть номер транзакції для видалення: ")) - 1
                deleted = tracker.delete_transaction(index)
                tracker.save_to_file()
                print(f"✅ Транзакцію '{deleted}' успішно видалено!")
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
            print(f"\n❌ Помилка файлової системи: {e}")
            input("\nНатисніть Enter, щоб продовжити...")

        except Exception as e:
            print(f"\n💥 Несподівана помилка: {e}")
            logger.critical(f"Неперехоплений виняток у CLI: {e}", exc_info=True)
            input("\nНатисніть Enter, щоб продовжити...")