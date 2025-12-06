# Personal Finance Manager

A command-line application for managing personal finances built with Python and Object-Oriented Programming principles.

## Features

### 1. Category Management
- Create custom income and expense categories
- Edit existing categories
- Delete categories (only if no transactions are associated)
- View all categories with type classification

### 2. Transaction Management
- Add new transactions (income/expense) with:
  - Amount
  - Category
  - Date (defaults to current date)
  - Unique auto-incremented ID
- Edit existing transactions by ID
- Delete transactions by ID
- Data validation for all inputs

### 3. Financial Reports & Analytics
- **Current Balance**: Total income minus total expenses
- **Category Statistics**: Breakdown of income and expenses by category
- **Popular Expense Categories**: Top 3 expense categories
- **Transaction History**: View last 10 transactions
- **Filter Transactions**: Filter by category, type, date range

### 4. Data Persistence
- **Auto-save/Load**: Automatically saves and loads from `finance_data.json`
- **Manual Save/Load**: Option to save/load from custom filenames
- **JSON Format**: Human-readable data storage

## Project Structure

```
finance_manager.py    # Main application file
finance_data.json     # Data storage file (auto-created)
```

## Classes

### Category Class
Stores category information:
- Category name
- Type (Income/Expense)

### Transaction Class
Stores transaction details:
- Unique ID
- Amount
- Category
- Date
- Type (Income/Expense)

### FinanceManager Class
Core business logic:
- Manages collections of categories and transactions
- Handles all CRUD operations
- Generates reports
- Manages data persistence

### UserInterface Class
Handles user interaction:
- Menu navigation
- Input validation
- Data display formatting

## Installation

1. **Prerequisites**:
   - Python 3.6 or higher
   - No external dependencies required

2. **Clone or Download**:
   ```bash
   git clone <repository-url>
   cd personal-finance-manager
   ```

3. **Run the Application**:
   ```bash
   python finance_manager.py
   ```

## Usage Guide

### Starting the Application
```bash
python finance_manager.py
```
The application will automatically load existing data from `finance_data.json` if available.

### Main Menu Options

| Option | Description |
|--------|-------------|
| 1 | Add new category |
| 2 | Delete category |
| 3 | Edit category |
| 4 | View all categories |
| 5 | Add new transaction |
| 6 | Edit transaction |
| 7 | Delete transaction |
| 8 | View balance and reports |
| 9 | Save data |
| 10 | Load data |
| 0 | Exit |

### Default Categories
On first run, the application creates these default categories:
- **Income**: Salary
- **Expenses**: Groceries, Transportation, Entertainment, Utilities

### Data Format
Transactions are stored with the following structure:
```json
{
  "categories": [
    {"name": "Salary", "type": "доход"},
    {"name": "Groceries", "type": "расход"}
  ],
  "transactions": [
    {
      "id": 1,
      "amount": 5000.0,
      "category": "Salary",
      "date": "2024-01-15",
      "type": "доход"
    }
  ],
  "next_id": 2
}
```

## OOP Concepts Demonstrated

This project showcases several Object-Oriented Programming principles:

### 1. **Encapsulation**
- Each class has well-defined responsibilities
- Internal data structures are protected
- Public methods provide controlled access

### 2. **Data Classes**
- Using Python's `@dataclass` decorator for clean data structures
- Automatic `__init__`, `__repr__`, and comparison methods

### 3. **Separation of Concerns**
- `FinanceManager`: Business logic and data management
- `UserInterface`: User interaction and display
- `Category`/`Transaction`: Data models

### 4. **JSON Serialization/Deserialization**
- Custom `to_dict()` and `from_dict()` methods
- Type-safe data conversion
- Enum handling for transaction types

### 5. **Error Handling**
- Input validation
- Graceful error recovery
- User-friendly error messages

## Learning Outcomes

This project helps understand:
- Class design and relationships
- Managing collections (lists, dictionaries)
- File I/O operations with JSON
- Business logic implementation
- User interface design for CLI applications
- Data persistence strategies

## Examples

### Adding a Transaction
```
МЕНЕДЖЕР ЛИЧНЫХ ФИНАНСОВ
==================================================
Выберите действие: 5

Добавление транзакции
Доступные категории:

Список категорий:
--------------------------------------------------
Название             Тип
--------------------------------------------------
Зарплата             +доход
Продукты             -расход
Транспорт            -расход
Развлечения          -расход
Коммунальные услуги  -расход
--------------------------------------------------

Введите категорию: Продукты
Введите сумму: 1500
Введите дату (ГГГГ-ММ-ДД) [сегодня]: 2024-01-20
Тип транзакции:
1. Доход
2. Расход
Выберите тип (1-2): 2

Транзакция успешно добавлена! ID: 1
```

### Viewing Reports
```
ФИНАНСОВЫЙ ОТЧЕТ
==================================================

Общий баланс: 3500.00 руб.
Общие доходы: 5000.00 руб.
Общие расходы: 1500.00 руб.

Доходы по категориям:
  Зарплата: 5000.00 руб.

Расходы по категориям:
  Продукты: 1500.00 руб.

Популярные категории расходов:
  1. Продукты: 1500.00 руб.

Последние транзакции:
--------------------------------------------------------
Дата        Категория            Тип       Сумма      ID
--------------------------------------------------------
2024-01-20  Продукты             -расход   1500.00    2
2024-01-15  Зарплата             +доход    5000.00    1
--------------------------------------------------------
```

## Extending the Project

The modular design makes it easy to extend:

### Adding New Features
1. **Budget Tracking**: Add budget limits to categories
2. **Recurring Transactions**: Implement scheduled transactions
3. **Data Export**: Add CSV/Excel export functionality
4. **Graphical Reports**: Integrate with matplotlib for charts
5. **Multi-currency Support**: Add currency conversion

### Code Modification Points
- `FinanceManager.generate_report()`: Add new report types
- `UserInterface.display_menu()`: Add new menu options
- `Transaction` class: Add new fields (notes, tags, etc.)
- JSON schema: Update data structure as needed

## Troubleshooting

### Common Issues

1. **"Категория не найдена" (Category not found)**
   - Ensure the category exists before adding transactions
   - Use option 4 to view all available categories

2. **File Permission Errors**
   - Check write permissions in the current directory
   - Try running as administrator if needed

3. **JSON File Corruption**
   - Backup `finance_data.json` regularly
   - The application creates a new file if corrupted

4. **Date Format Errors**
   - Always use YYYY-MM-DD format (e.g., 2024-01-20)

## License

This project is created for educational purposes. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository
