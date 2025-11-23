# Cхемы

from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class DepartmentBase(BaseModel):
    name: str

class Department(DepartmentBase):
    id: int
    class Config:
        orm_mode = True


class PositionBase(BaseModel):
    name: str

class Position(PositionBase):
    id: int
    class Config:
        orm_mode = True


class SalaryHistoryBase(BaseModel):
    change_date: date
    amount: float

class SalaryHistory(SalaryHistoryBase):
    id: int
    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    hire_date: date
    department_id: int
    position_id: int

class Employee(EmployeeBase):
    id: int
    department: Department
    position: Position
    class Config:
        orm_mode = True