from pathlib import Path
current_file = Path(__file__)
current_dir = Path(__file__).parent


data_dir = current_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)
incomes = data_dir / "incomes.txt"
expenses = data_dir / "expenses.txt"
transactions = data_dir / "transactions.txt"

while True:
    print("\nМеню:")
    print("1. Додати дохід")
    print("2. Додати витрату")
    print("3. Переглянути транзакції")
    print("4. Видалити транзакцію")
    print("5. Вихід")

    choice = input("Оберіть пункт меню (1-5): ")

    if choice == "1":
        amount = input("Введіть суму доходу: ")
        description = input("Введіть опис: ")
        transaction_income = f"{amount},{description}\n"
        with open(incomes, "a", encoding="utf-8") as f:
            f.write(transaction_income)
        print(f"Додано дохід: {amount} грн ({description})")
        
    elif choice == "2":
        amount = input("Введіть суму витрати: ")
        description = input("Введіть опис: ")
        transaction_expenses = f"{amount},{description}\n"
        with open(expenses, "a", encoding="utf-8") as f:
            f.write(transaction_expenses)
        print(f"Додано витрату: {amount} грн ({description})")

    elif choice == "3":        
        print("\n--- Доходи ---")
        with open(incomes, "r", encoding="utf-8") as f:
            print(f.read())
            
        print("--- Витрати ---")
        with open(expenses, "r", encoding="utf-8") as f:
            print(f.read())
    elif choice == "4":
        print()
        
    elif choice == "5":
        print("Вихід з програми. До побачення!")
        break
        
    else:
        print("Невірний вибір. Введіть число від 1 до 5.")