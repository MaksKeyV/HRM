
from sqlalchemy.orm import Session
from models import Employee, Department, Position, SalaryHistory
from schemas import EmployeeBase, DepartmentBase, PositionBase, SalaryHistoryBase


"""
Функция получает список всех отделов
    Параметры: db: Session — объект SQLAlchemy
    Возвращаемое значение: list[Department] — список отделов
"""
def get_departments(db: Session):
    return db.query(Department).all()   # Выполняем запрос всех отделов из таблицы Department


"""
Функция получает список всех должностей
    Параметры: b: Session — объект SQLAlchemy
    Возвращаемое значение: list[Position] — список должностей
"""
def get_positions(db: Session):
    return db.query(Position).all()  # Выполняем запрос всех должностей из таблицы Position


"""
Функция получает список сотрудников с возможной фильтрацией
    Параметры: 
        db: Session — объект SQLAlchemy
        dept: int | None — id отдела для фильтрации
        pos: int | None — id должности для фильтрации
        date_from: date | None — дата найма (начало)
        date_to: date | None — дата найма (конец)
    Возвращаемое значение: list[Employee] — список сотрудников с текущей зарплатой
"""
def get_employees(db: Session, dept = None, pos = None, date_from = None, date_to = None):
    query = db.query(Employee) # Создаём запрос к таблице сотрудников

    if dept:
        query = query.filter(Employee.department_id == dept) # Фильтруем по отделу
    if pos:
        query = query.filter(Employee.position_id == pos) # Фильтруем по должности
    if date_from:
        query = query.filter(Employee.hire_date >= date_from) # Фильтруем по дате найма с начала
    if date_to:
        query = query.filter(Employee.hire_date <= date_to) # Фильтруем по дате найма до конца

    employees = query.all()  # Выполняем запрос и получаем список сотрудников

    # Добавляем текущую зарплату для каждого сотрудника
    for e in employees:
        if e.salary_history: # Если есть история зарплаты
            e.current_salary = max(h.amount for h in e.salary_history) # Берём максимальную зарплату
        else:   # Иначе оставляем пустое значение
            e.current_salary = None

    return employees


"""
Функция получает историю зарплат указанного сотрудника
    Параметры: 
        db: Session — объект сессии SQLAlchemy
        employee_id: int — ID сотрудника
    Возвращаемое значение: list[SalaryHistory] — список записей истории зарплат
"""
def get_salary_history(db: Session, employee_id: int):
    # Выполняем запрос всех записей истории зарплат для конкретного сотрудника
    return db.query(SalaryHistory).filter(SalaryHistory.employee_id == employee_id).all()


