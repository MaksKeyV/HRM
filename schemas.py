
from pydantic import BaseModel
from datetime import date
from typing import Optional, List


"""
Класс DepartmentBase для описания отдела
"""
class DepartmentBase(BaseModel):
    name: str   # Название отдела


"""
Класс Department для передачи отдела с id
"""
class Department(DepartmentBase):
    id: int  # id отдела

    class Config:
        orm_mode = True # Включаем режим ORM для работы с объектами SQLAlchemy


"""
Класс PositionBase для описания должности
"""
class PositionBase(BaseModel):
    name: str  # Название должности


"""
Класс Position для передачи должности с id
"""
class Position(PositionBase):
    id: int  # id должности

    class Config:
        orm_mode = True # Включаем режим ORM для работы с объектами SQLAlchemy


"""
Класс SalaryHistoryBase для описания записи истории зарплаты
"""
class SalaryHistoryBase(BaseModel):
    change_date: date  # Дата изменения зарплаты
    amount: float      # Размер зарплаты после изменения


"""
Класс SalaryHistory для возврата записи с id и employee_id
"""
class SalaryHistory(SalaryHistoryBase):
    id: int                # id записи
    employee_id: int       # id сотрудника

    class Config:
        orm_mode = True # Включаем режим ORM для работы с объектами SQLAlchemy


"""
Класс EmployeeBase для описания сотрудника
"""
class EmployeeBase(BaseModel):
    last_name: str         # Фамилия
    first_name: str        # Имя
    middle_name: Optional[str] = None  # Отчество
    hire_date: date        # Дата приема
    


"""
Класс Employee для передачи сотрудника с отделом, должностью и текущей зарплатой
"""
class Employee(EmployeeBase):
    id: int                              # id сотрудника
    department: Department               # Объект отдела
    position: Position                   # Объект должности
    current_salary: Optional[float] = None  # Текущая зарплата

    class Config:
        orm_mode = True # Включаем режим ORM для работы с объектами SQLAlchemy


"""
Класс EmployeeCreate для создания нового сотрудника
"""
class EmployeeCreate(EmployeeBase):
    department_id: int     # id отдела
    position_id: int       # id должности
    amount: float  # Начальная зарплата


"""
Класс EmployeeFull — расширенная информация о сотруднике
"""
class EmployeeFull(BaseModel):
    id: int   # Уникальный идентификатор сотрудника
    last_name: str  # Фамилия сотрудника
    first_name: str  # Имя сотрудника
    middle_name: Optional[str] = None  # Отчество сотрудника
    hire_date: date  # Дата найма сотрудника
    department: Optional[str]  # Название отдела
    position: Optional[str]  # Название должности
    current_salary: Optional[float] = None  # Текущая зарплата

    class Config:
        orm_mode = True # Включаем режим ORM для работы с объектами SQLAlchemy
