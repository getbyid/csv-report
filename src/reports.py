import csv
from abc import ABC, abstractmethod
from typing import Any, Iterable

from .database import Database


class BaseReport(ABC):
    """
    Новые отчёты добавляются наследованием этого базового класса.
    `report_type` - слово (строка), по которому пользователь выбирает тип отчёта
    """

    report_type = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ReportsRegistry.register(cls)

    def __init__(self):
        self.db = Database()
        self.db.create_schema()

    def add_employees(self, file: str):
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.db.insert_employee(row)

    @property
    @abstractmethod
    def headers(self) -> list[str]:
        pass

    @abstractmethod
    def make(self) -> list[Iterable[Any]]:
        pass


class ReportsRegistry:
    """
    Реестр отчётов с авторегистрацией при импорте реализаций
    """

    _items = []

    @classmethod
    def register(cls, item):
        cls._items.append(item)

    @classmethod
    def keys(cls):
        return [str(item.report_type) for item in cls._items]

    @classmethod
    def get(cls, key) -> BaseReport | None:
        for item in cls._items:
            if item.report_type == key:
                return item()


class PerformanceReport(BaseReport):
    """
    Позиция и средняя эффективность (среднее арифметическое по performance),
    сортировка по эффективности
    """

    report_type = "performance"

    @property
    def headers(self):
        return ("", "position", "performance")

    def make(self):
        return self.db.select_performance()
