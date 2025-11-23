# Таблицы SQL

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    employees = relationship("Employee", back_populates="department")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    hire_date = Column(Date)

    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    salary_history = relationship("SalaryHistory", back_populates="employee")


class SalaryHistory(Base):
    __tablename__ = "salary_history"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    change_date = Column(Date)
    amount = Column(Float)

    employee = relationship("Employee", back_populates="salary_history")