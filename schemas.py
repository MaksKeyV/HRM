
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
    id: int # id отдела
    class Config:
        orm_mode = True 


"""
Класс PositionBase для описания должности
"""
class PositionBase(BaseModel):
    name: str    # Название должности

"""
Класс Position для передачи должности с id
"""
class Position(PositionBase):
    id: int # id должности
    class Config:
        orm_mode = True

"""
Класс SalaryHistoryBase для описания записи истории зарплаты
"""
class SalaryHistoryBase(BaseModel):
    change_date: date   # Дата изменения зарплаты
    amount: float    # Сумма зарплаты после изменения


"""
Класс SalaryHistory для передачи записи истории зарплаты с id
"""
class SalaryHistory(SalaryHistoryBase):
    id: int # id записи истории зарплаты
    class Config:
        orm_mode = True

"""
Класс EmployeeBase для описания сотрудника
"""
class EmployeeBase(BaseModel):
    last_name: str       # Фамилия сотрудника
    first_name: str      # Имя сотрудника
    middle_name: Optional[str] = None  # Отчество сотрудника
    hire_date: date      # Дата приёма на работу
    department_id: int   # id отдела сотрудника
    position_id: int     # id должности сотрудника

"""
Класс Employee для передачи сотрудника с id, отделом, должностью и текущей зарплатой
"""
class Employee(EmployeeBase):
    id: int                       # Уникальный идентификатор сотрудника
    department: Department        # Отдел, к которому принадлежит сотрудник
    position: Position            # Должность сотрудника
    current_salary: Optional[float] = None  # Текущая зарплата, может отсутствовать
    class Config:
        orm_mode = True

class EmployeeCreate(EmployeeBase):
    amount: float  # начальная зарплата