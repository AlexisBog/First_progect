class ExpenseTrackerError(Exception):
    """Базовий клас для всіх помилок трекера."""
    pass

class InvalidAmountError(ExpenseTrackerError):
    """Викликається, якщо сума від'ємна або дорівнює нулю."""
    pass

class TransactionNotFoundError(ExpenseTrackerError):
    """Викликається, якщо транзакцію не знайдено."""
    pass

class DataStorageError(ExpenseTrackerError):
    """Викликається при помилках читання/запису JSON."""
    pass