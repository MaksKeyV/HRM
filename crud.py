# Функции для работы с базой

from sqlalchemy.orm import Session
from models import Employee, Department, Position, SalaryHistory
from schemas import EmployeeBase, DepartmentBase, PositionBase, SalaryHistoryBase


# ====== DEPARTMENTS ======
def get_departments(db: Session):
    return db.query(Department).all()


# ====== POSITIONS ======
def get_positions(db: Session):
    return db.query(Position).all()


# ====== EMPLOYEES ======
def get_employees(db: Session, dept=None, pos=None, date_from=None, date_to=None):
    query = db.query(Employee)

    if dept:
        query = query.filter(Employee.department_id == dept)
    if pos:
        query = query.filter(Employee.position_id == pos)
    if date_from:
        query = query.filter(Employee.hire_date >= date_from)
    if date_to:
        query = query.filter(Employee.hire_date <= date_to)

    return query.all()


# ====== SALARY HISTORY ======
def get_salary_history(db: Session, employee_id: int):
    return db.query(SalaryHistory).filter(SalaryHistory.employee_id == employee_id).all()