import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum


class TransactionType(Enum):
    INCOME = "доход"
    EXPENSE = "расход"


@dataclass
class Category:
    name: str
    type: TransactionType
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        return cls(
            name=data["name"],
            type=TransactionType(data["type"])
        )


@dataclass
class Transaction:
    amount: float
    category: str
    date: str
    type: TransactionType
    id: int = 0
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "type": self.type.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        return cls(
            id=data["id"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            type=TransactionType(data["type"])
        )


class FinanceManager:
    def __init__(self):
        self.categories: Dict[str, Category] = {}
        self.transactions: List[Transaction] = []
        self.next_id: int = 1
        
        # Создаем начальные категории
        self._create_default_categories()
    
    def _create_default_categories(self):
        """Создание базовых категорий"""
        default_categories = [
            Category("Зарплата", TransactionType.INCOME),
            Category("Продукты", TransactionType.EXPENSE),
            Category("Транспорт", TransactionType.EXPENSE),
            Category("Развлечения", TransactionType.EXPENSE),
            Category("Коммунальные услуги", TransactionType.EXPENSE),
        ]
        
        for category in default_categories:
            self.add_category(category)
    
    def add_category(self, category: Category) -> bool:
        """Добавление новой категории"""
        if category.name in self.categories:
            return False
        self.categories[category.name] = category
        return True
    
    def remove_category(self, category_name: str) -> bool:
        """Удаление категории"""
        if category_name not in self.categories:
            return False
        
        # Проверяем, есть ли транзакции с этой категорией
        for transaction in self.transactions:
            if transaction.category == category_name:
                return False  # Нельзя удалить категорию с транзакциями
        
        del self.categories[category_name]
        return True
    
    def edit_category(self, old_name: str, new_name: str, new_type: TransactionType) -> bool:
        """Редактирование категории"""
        if old_name not in self.categories:
            return False
        
        # Проверяем, существует ли новая категория
        if new_name in self.categories and new_name != old_name:
            return False
        
        category = self.categories.pop(old_name)
        category.name = new_name
        category.type = new_type
        self.categories[new_name] = category
        
        # Обновляем категории в транзакциях
        for transaction in self.transactions:
            if transaction.category == old_name:
                transaction.category = new_name
        
        return True
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Добавление новой транзакции"""
        # Проверяем существование категории
        if transaction.category not in self.categories:
            return False
        
        # Проверяем тип категории
        category_type = self.categories[transaction.category].type
        if category_type != transaction.type:
            return False
        
        # Присваиваем уникальный ID
        transaction.id = self.next_id
        self.next_id += 1
        self.transactions.append(transaction)
        return True
    
    def edit_transaction(self, transaction_id: int, new_data: dict) -> bool:
        """Редактирование транзакции"""
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                # Проверяем существование новой категории
                if 'category' in new_data and new_data['category'] not in self.categories:
                    return False
                
                # Проверяем тип категории
                if 'category' in new_data and 'type' in new_data:
                    category_type = self.categories[new_data['category']].type
                    if category_type != new_data['type']:
                        return False
                
                # Обновляем данные
                for key, value in new_data.items():
                    if hasattr(transaction, key):
                        setattr(transaction, key, value)
                return True
        return False
    
    def remove_transaction(self, transaction_id: int) -> bool:
        """Удаление транзакции"""
        for i, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                self.transactions.pop(i)
                return True
        return False
    
    def get_balance(self) -> float:
        """Расчет общего баланса"""
        balance = 0.0
        for transaction in self.transactions:
            if transaction.type == TransactionType.INCOME:
                balance += transaction.amount
            else:
                balance -= transaction.amount
        return balance
    
    def generate_report(self) -> dict:
        """Формирование отчета"""
        report = {
            "total_balance": self.get_balance(),
            "income_by_category": {},
            "expense_by_category": {},
            "total_income": 0,
            "total_expense": 0,
            "popular_expense_categories": [],
            "transaction_history": []
        }
        
        # Собираем статистику по категориям
        for transaction in self.transactions:
            category_stats = (
                report["income_by_category"] 
                if transaction.type == TransactionType.INCOME 
                else report["expense_by_category"]
            )
            
            if transaction.category not in category_stats:
                category_stats[transaction.category] = 0
            category_stats[transaction.category] += transaction.amount
            
            # Суммируем общие доходы и расходы
            if transaction.type == TransactionType.INCOME:
                report["total_income"] += transaction.amount
            else:
                report["total_expense"] += transaction.amount
        
        # Определяем популярные категории расходов
        if report["expense_by_category"]:
            sorted_categories = sorted(
                report["expense_by_category"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            report["popular_expense_categories"] = [
                {"category": cat, "amount": amount}
                for cat, amount in sorted_categories[:3]  # Топ-3 категории
            ]
        
        # История транзакций (последние 10)
        sorted_transactions = sorted(
            self.transactions,
            key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"),
            reverse=True
        )
        
        report["transaction_history"] = [
            {
                "id": t.id,
                "date": t.date,
                "category": t.category,
                "type": t.type.value,
                "amount": t.amount
            }
            for t in sorted_transactions[:10]
        ]
        
        return report
    
    def get_categories_by_type(self, type_filter: Optional[TransactionType] = None) -> List[Category]:
        """Получение категорий с фильтром по типу"""
        if type_filter is None:
            return list(self.categories.values())
        return [cat for cat in self.categories.values() if cat.type == type_filter]
    
    def get_transactions(self, 
                        category_filter: Optional[str] = None,
                        type_filter: Optional[TransactionType] = None,
                        date_from: Optional[str] = None,
                        date_to: Optional[str] = None) -> List[Transaction]:
        """Получение транзакций с фильтрами"""
        filtered = self.transactions
        
        if category_filter:
            filtered = [t for t in filtered if t.category == category_filter]
        
        if type_filter:
            filtered = [t for t in filtered if t.type == type_filter]
        
        if date_from:
            filtered = [t for t in filtered if t.date >= date_from]
        
        if date_to:
            filtered = [t for t in filtered if t.date <= date_to]
        
        return filtered
    
    def save_to_file(self, filename: str) -> bool:
        """Сохранение данных в JSON файл"""
        try:
            data = {
                "categories": [
                    category.to_dict() for category in self.categories.values()
                ],
                "transactions": [
                    transaction.to_dict() for transaction in self.transactions
                ],
                "next_id": self.next_id
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Загрузка данных из JSON файла"""
        try:
            if not os.path.exists(filename):
                return False
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загружаем категории
            self.categories.clear()
            for cat_data in data.get("categories", []):
                category = Category.from_dict(cat_data)
                self.categories[category.name] = category
            
            # Загружаем транзакции
            self.transactions.clear()
            for trans_data in data.get("transactions", []):
                transaction = Transaction.from_dict(trans_data)
                self.transactions.append(transaction)
            
            # Устанавливаем следующий ID
            self.next_id = data.get("next_id", 1)
            
            # Обновляем next_id если нужно
            if self.transactions:
                max_id = max(t.id for t in self.transactions)
                self.next_id = max(self.next_id, max_id + 1)
            
            return True
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return False


class UserInterface:
    @staticmethod
    def display_menu():
        """Отображение главного меню"""
        print("\n" + "="*50)
        print("МЕНЕДЖЕР ЛИЧНЫХ ФИНАНСОВ")
        print("="*50)
        print("1. Добавить категорию")
        print("2. Удалить категорию")
        print("3. Редактировать категорию")
        print("4. Просмотреть категории")
        print("5. Добавить транзакцию")
        print("6. Редактировать транзакцию")
        print("7. Удалить транзакцию")
        print("8. Просмотр баланса и отчетов")
        print("9. Сохранить данные")
        print("10. Загрузить данные")
        print("0. Выход")
        print("="*50)
    
    @staticmethod
    def get_input(prompt: str, default: str = "") -> str:
        """Получение ввода от пользователя"""
        result = input(prompt)
        return result if result else default
    
    @staticmethod
    def display_categories(categories: List[Category]):
        """Отображение списка категорий"""
        if not categories:
            print("Нет категорий.")
            return
        
        print("\nСписок категорий:")
        print("-" * 50)
        print(f"{'Название':<20} {'Тип':<10}")
        print("-" * 50)
        
        for category in categories:
            type_icon = "+" if category.type == TransactionType.INCOME else "-"
            print(f"{category.name:<20} {type_icon}{category.type.value:<9}")
        print("-" * 50)
    
    @staticmethod
    def display_report(report: dict):
        """Отображение отчета"""
        print("\n" + "="*50)
        print("ФИНАНСОВЫЙ ОТЧЕТ")
        print("="*50)
        
        print(f"\nОбщий баланс: {report['total_balance']:.2f} руб.")
        print(f"Общие доходы: {report['total_income']:.2f} руб.")
        print(f"Общие расходы: {report['total_expense']:.2f} руб.")
        
        if report['income_by_category']:
            print("\nДоходы по категориям:")
            for category, amount in report['income_by_category'].items():
                print(f"  {category}: {amount:.2f} руб.")
        
        if report['expense_by_category']:
            print("\nРасходы по категориям:")
            for category, amount in report['expense_by_category'].items():
                print(f"  {category}: {amount:.2f} руб.")
        
        if report['popular_expense_categories']:
            print("\nПопулярные категории расходов:")
            for i, item in enumerate(report['popular_expense_categories'], 1):
                print(f"  {i}. {item['category']}: {item['amount']:.2f} руб.")
        
        if report['transaction_history']:
            print("\nПоследние транзакции:")
            print("-" * 60)
            print(f"{'Дата':<12} {'Категория':<20} {'Тип':<10} {'Сумма':<10} {'ID':<5}")
            print("-" * 60)
            for trans in report['transaction_history']:
                type_icon = "+" if trans['type'] == "доход" else "-"
                print(f"{trans['date']:<12} {trans['category']:<20} "
                      f"{type_icon}{trans['type']:<9} {trans['amount']:<10.2f} {trans['id']:<5}")
            print("-" * 60)
    
    @staticmethod
    def display_transactions(transactions: List[Transaction]):
        """Отображение списка транзакций"""
        if not transactions:
            print("Нет транзакций.")
            return
        
        print("\nСписок транзакций:")
        print("-" * 60)
        print(f"{'ID':<5} {'Дата':<12} {'Категория':<20} {'Тип':<10} {'Сумма':<10}")
        print("-" * 60)
        
        for transaction in transactions:
            type_icon = "+" if transaction.type == TransactionType.INCOME else "-"
            print(f"{transaction.id:<5} {transaction.date:<12} "
                  f"{transaction.category:<20} {type_icon}{transaction.type.value:<9} "
                  f"{transaction.amount:<10.2f}")
        print("-" * 60)


def main():
    """Главная функция программы"""
    manager = FinanceManager()
    ui = UserInterface()
    filename = "finance_data.json"
    
    # Пытаемся загрузить сохраненные данные
    if manager.load_from_file(filename):
        print("Данные успешно загружены.")
    
    while True:
        ui.display_menu()
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":  # Добавить категорию
            print("\nДобавление новой категории")
            name = ui.get_input("Название категории: ")
            
            print("Тип категории:")
            print("1. Доход")
            print("2. Расход")
            type_choice = ui.get_input("Выберите тип (1-2): ")
            
            if type_choice == "1":
                trans_type = TransactionType.INCOME
            elif type_choice == "2":
                trans_type = TransactionType.EXPENSE
            else:
                print("Неверный выбор типа!")
                continue
            
            category = Category(name, trans_type)
            if manager.add_category(category):
                print(f"Категория '{name}' успешно добавлена!")
            else:
                print("Ошибка: категория с таким названием уже существует!")
        
        elif choice == "2":  # Удалить категорию
            print("\nУдаление категории")
            ui.display_categories(list(manager.categories.values()))
            name = ui.get_input("Введите название категории для удаления: ")
            
            if manager.remove_category(name):
                print(f"Категория '{name}' успешно удалена!")
            else:
                print("Ошибка: категория не найдена или имеет связанные транзакции!")
        
        elif choice == "3":  # Редактировать категорию
            print("\nРедактирование категории")
            ui.display_categories(list(manager.categories.values()))
            old_name = ui.get_input("Введите название категории для редактирования: ")
            
            if old_name not in manager.categories:
                print("Категория не найдена!")
                continue
            
            new_name = ui.get_input(f"Новое название [{old_name}]: ", old_name)
            
            print("Новый тип категории:")
            print("1. Доход")
            print("2. Расход")
            current_type = manager.categories[old_name].type
            type_choice = ui.get_input(f"Выберите тип (1-2) [текущий: {current_type.value}]: ")
            
            if type_choice == "1":
                new_type = TransactionType.INCOME
            elif type_choice == "2":
                new_type = TransactionType.EXPENSE
            elif not type_choice:
                new_type = current_type
            else:
                print("Неверный выбор типа!")
                continue
            
            if manager.edit_category(old_name, new_name, new_type):
                print(f"Категория успешно обновлена!")
            else:
                print("Ошибка при обновлении категории!")
        
        elif choice == "4":  # Просмотреть категории
            print("\nКатегории доходов:")
            income_cats = manager.get_categories_by_type(TransactionType.INCOME)
            ui.display_categories(income_cats)
            
            print("\nКатегории расходов:")
            expense_cats = manager.get_categories_by_type(TransactionType.EXPENSE)
            ui.display_categories(expense_cats)
        
        elif choice == "5":  # Добавить транзакцию
            print("\nДобавление транзакции")
            
            # Показываем доступные категории
            print("Доступные категории:")
            ui.display_categories(list(manager.categories.values()))
            
            category = ui.get_input("Введите категорию: ")
            amount_str = ui.get_input("Введите сумму: ")
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Сумма должна быть положительной!")
                    continue
            except ValueError:
                print("Неверный формат суммы!")
                continue
            
            date_str = ui.get_input("Введите дату (ГГГГ-ММ-ДД) [сегодня]: ")
            if not date_str:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            print("Тип транзакции:")
            print("1. Доход")
            print("2. Расход")
            type_choice = ui.get_input("Выберите тип (1-2): ")
            
            if type_choice == "1":
                trans_type = TransactionType.INCOME
            elif type_choice == "2":
                trans_type = TransactionType.EXPENSE
            else:
                print("Неверный выбор типа!")
                continue
            
            transaction = Transaction(amount, category, date_str, trans_type)
            if manager.add_transaction(transaction):
                print(f"Транзакция успешно добавлена! ID: {transaction.id}")
            else:
                print("Ошибка: проверьте правильность категории и её типа!")
        
        elif choice == "6":  # Редактировать транзакцию
            print("\nРедактирование транзакции")
            ui.display_transactions(manager.transactions)
            
            try:
                trans_id = int(ui.get_input("Введите ID транзакции для редактирования: "))
            except ValueError:
                print("Неверный формат ID!")
                continue
            
            new_data = {}
            
            # Получаем новые данные
            new_category = ui.get_input("Новая категория (оставьте пустым для сохранения текущей): ")
            if new_category:
                new_data['category'] = new_category
            
            new_amount = ui.get_input("Новая сумма (оставьте пустым для сохранения текущей): ")
            if new_amount:
                try:
                    new_data['amount'] = float(new_amount)
                except ValueError:
                    print("Неверный формат суммы!")
                    continue
            
            new_date = ui.get_input("Новая дата (ГГГГ-ММ-ДД) (оставьте пустым для сохранения текущей): ")
            if new_date:
                new_data['date'] = new_date
            
            if not new_data:
                print("Ничего не изменено!")
                continue
            
            if manager.edit_transaction(trans_id, new_data):
                print("Транзакция успешно обновлена!")
            else:
                print("Ошибка при обновлении транзакции!")
        
        elif choice == "7":  # Удалить транзакцию
            print("\nУдаление транзакции")
            ui.display_transactions(manager.transactions)
            
            try:
                trans_id = int(ui.get_input("Введите ID транзакции для удаления: "))
            except ValueError:
                print("Неверный формат ID!")
                continue
            
            if manager.remove_transaction(trans_id):
                print("Транзакция успешно удалена!")
            else:
                print("Транзакция с указанным ID не найдена!")
        
        elif choice == "8":  # Просмотр баланса и отчетов
            report = manager.generate_report()
            ui.display_report(report)
            
            # Дополнительные опции
            print("\nДополнительные опции:")
            print("1. Показать все транзакции")
            print("2. Фильтровать транзакции")
            print("0. Назад")
            
            sub_choice = ui.get_input("Выберите опцию: ")
            
            if sub_choice == "1":
                ui.display_transactions(manager.transactions)
            elif sub_choice == "2":
                print("\nФильтрация транзакций")
                print("Оставьте поле пустым, чтобы пропустить фильтр")
                
                category = ui.get_input("Категория: ")
                if category == "":
                    category = None
                
                print("Тип:")
                print("1. Доход")
                print("2. Расход")
                print("0. Любой")
                type_choice = ui.get_input("Выберите тип: ")
                
                if type_choice == "1":
                    type_filter = TransactionType.INCOME
                elif type_choice == "2":
                    type_filter = TransactionType.EXPENSE
                else:
                    type_filter = None
                
                date_from = ui.get_input("Дата от (ГГГГ-ММ-ДД): ")
                if date_from == "":
                    date_from = None
                
                date_to = ui.get_input("Дата до (ГГГГ-ММ-ДД): ")
                if date_to == "":
                    date_to = None
                
                filtered = manager.get_transactions(category, type_filter, date_from, date_to)
                ui.display_transactions(filtered)
        
        elif choice == "9":  # Сохранить данные
            if manager.save_to_file(filename):
                print(f"Данные успешно сохранены в файл {filename}")
            else:
                print("Ошибка при сохранении данных!")
        
        elif choice == "10":  # Загрузить данные
            filename_input = ui.get_input(f"Введите имя файла [{filename}]: ", filename)
            if manager.load_from_file(filename_input):
                print("Данные успешно загружены!")
            else:
                print("Ошибка при загрузке данных!")
        
        elif choice == "0":  # Выход
            # Предлагаем сохранить перед выходом
            save_choice = ui.get_input("Сохранить данные перед выходом? (y/n): ")
            if save_choice.lower() == 'y':
                manager.save_to_file(filename)
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
