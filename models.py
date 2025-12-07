
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base


"""
Класс Department описывает таблицу отделов
"""
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key = True)   # id отдела
    name = Column(String(100), unique = True) # Название отдела

    # Связь один-ко-многим: один отдел — много сотрудников
    employees = relationship("Employee", back_populates="department")


"""
Класс Position описывает таблицу должностей
"""
class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key = True)  # id должности
    name = Column(String(100), unique = True) # Название должности

     # Связь один-ко-многим с сотрудниками
    employees = relationship("Employee", back_populates="position")


"""
Класс Employee описывает таблицу сотрудников
"""
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key = True)  # id сотрудника
    last_name = Column(String(120))  # Фамилия сотрудника
    first_name = Column(String(120))  # Имя сотрудника
    middle_name = Column(String(120))  # отчество сотрудника
    hire_date = Column(Date)  # Дата приёма на работу

    department_id = Column(Integer, ForeignKey("departments.id"))   # Связь с отделом
    position_id = Column(Integer, ForeignKey("positions.id"))    # Связь с должностью

    # Связь многие-к-одному с отделом
    department = relationship("Department", back_populates="employees")

    # Связь многие-к-одному с должностью
    position = relationship("Position", back_populates="employees")

    # Связь один-ко-многим с историей зарплат
    salary_history = relationship("SalaryHistory", back_populates="employee")


"""
Класс SalaryHistory описывает таблицу истории зарплат
"""
class SalaryHistory(Base):
    __tablename__ = "salary_history"

    id = Column(Integer, primary_key = True)    # Уникальный идентификатор записи истории зарплаты
    employee_id = Column(Integer, ForeignKey("employees.id"))  # Связь с сотрудником
    change_date = Column(Date)  # Дата изменения зарплаты
    amount = Column(Float)  # Зарплата

    # Связь многие-к-одному с сотрудником
    employee = relationship("Employee", back_populates = "salary_history")
