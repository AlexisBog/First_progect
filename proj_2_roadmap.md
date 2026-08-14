# ROADMAP Project 2: Expense and Budget Tracker

## Що має виходити після кожного модуля

# Module 1. Python Basics + Git

**Теми:** синтаксис, змінні, умови, цикли, функції, Git basics

## Що зробити

Створити просту CLI-програму для обліку доходів та витрат.

## Мінімальний функціонал

Користувач може:

* додати дохід;
* додати витрату;
* переглянути всі транзакції;
* видалити транзакцію.

## Приклад CLI

```bash
python main.py
```

Меню:

```text
1. Add income
2. Add expense
3. Show transactions
4. Delete transaction
5. Exit
```

## Структура транзакції

```python
transaction = {
    "amount": 1000,
    "type": "income",
    "category": "Salary"
}
```

## Що практикуємо

* input()
* print()
* if/elif
* while
* functions
* lists/dicts

## Git

Repository:

```bash
git init
git add .
git commit -m "lesson 1-7 expense tracker"
```

## Результат модуля

CLI expense tracker без збереження даних.

# Module 2. Python Core / OOP

**Теми:** classes, inheritance, exceptions, modules

## Що зробити

Переписати застосунок на класи.

## Створити класи

```python
User
Transaction
Budget
ExpenseTracker
```

## Transaction model

```python
amount
transaction_type
category
date
description
```

## Додати методи

* add_transaction()
* delete_transaction()
* list_transactions()
* calculate_balance()
* monthly_report()

## Exceptions

Обробляти:

```python
Invalid amount
Transaction not found
Invalid menu choice
```

## Результат модуля

ООП фінансовий менеджер.

# Module 3. Files + Advanced Python

**Теми:** JSON, CSV, decorators, typing, virtualenv, pip

## Що зробити

Додати збереження транзакцій.

## Storage

Файли:

```text
transactions.json
transactions.csv
```

## Поведінка програми

* load transactions from JSON
* save transactions to JSON

## CSV export

```python
export_to_csv()
```

## Typing

```python
def add_transaction(amount: float, category: str) -> None:
```

## Decorators

```python
@log_transaction
```

## Результат

Дані зберігаються між запусками.

# Module 4. Testing + HTTP

**Теми:** pytest, requests, mocking

## Що зробити

Покрити бізнес-логіку тестами.

## Тести

* add_transaction
* delete_transaction
* calculate_balance
* monthly_report

## HTTP integration

Інтеграція з API курсів валют.

Можливості:

* отримання курсу валют;
* конвертація USD/EUR/UAH.

## Приклад

```python
get_exchange_rate("USD", "UAH")
```

## Результат

Unit tests + currency API.

# Module 5. Databases

**Теми:** SQLite, SQL, PostgreSQL

## Що зробити

Перенести збереження з JSON у базу даних.

## Таблиці

### users

* id
* username
* email

### transactions

* id
* amount
* transaction_type
* category
* date
* description
* user_id

### budgets

* id
* category
* monthly_limit
* user_id

## SQL operations

* INSERT
* UPDATE
* DELETE
* SELECT
* GROUP BY
* SUM

## Нові можливості

* budget per category
* monthly spending analytics

## Результат

Проєкт працює через БД.

# Module 6. Django Basics

**Теми:** Django models/views/templates/forms/admin

## Що зробити

Перетворити CLI на web app.

## Pages

### Authentication

* login
* register
* logout

### Transactions

* transaction list
* add transaction
* edit transaction
* delete transaction

### Reports

* monthly report
* balance summary

### Budgets

* create budget
* edit budget

## Django Admin

Керування:

* users
* transactions
* budgets

## Результат

Web expense tracker.

# Module 7. Django REST Framework

**Теми:** serializers, viewsets, routers, permissions

## Що зробити

Створити API.

## Endpoints

```text
/api/transactions/
/api/budgets/
/api/users/
```

## CRUD

* GET
* POST
* PUT
* DELETE

## Authentication

* token auth

## Результат

REST API для фінансового застосунку.

# Module 8. Final Improvements / Deploy Prep

**Теми:** refactoring, documentation, deployment prep

## Що зробити

Refactor:

* clean architecture
* split modules

## README

Описати:

* install
* run
* tests

## requirements.txt

```bash
pip freeze > requirements.txt
```

## Optional features

* charts/dashboard
* recurring payments
* export reports
* categories analytics
* notifications about budget limits

## Final project structure

```text
expense_tracker/
    src/
    tests/
    templates/
    static/
    requirements.txt
    README.md
```

# Що студент має в кінці

До завершення курсу студент отримує:

✅ Python CLI application
✅ OOP architecture
✅ JSON/CSV support
✅ pytest tests
✅ SQLite/PostgreSQL
✅ Django web app
✅ REST API
✅ GitHub portfolio project

# Візуальний прогрес

### Після module 1

консольний трекер транзакцій

### Після module 3

фінансовий менеджер із файлами

### Після module 5

DB-backed application

### Після module 7

mini finance manager web app
