
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import Base, engine, get_db
from schemas import (Employee, EmployeeCreate, Department, Position, SalaryHistory, SalaryHistoryBase, EmployeeFull)
from models import (Employee as EmployeeModel, Department as DepartmentModel, Position as PositionModel, SalaryHistory as SalaryHistoryModel)
import db_queries
from datetime import date

# Создаём приложение FastAPI
app = FastAPI()

# Разрешаем доступ к API с любых источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Разрешаем запросы с любых доменов
    allow_methods=["*"],   # Разрешаем все HTTP-методы
    allow_headers=["*"]    # Разрешаем все заголовки
)

Base.metadata.create_all(bind = engine)   # Создаём все таблицы в базе, если их ещё нет


"""
Функция получает все отделы из базы данных
    Параметры: db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: list[Department] — список отделов
"""
@app.get("/departments", response_model = List[Department])
def read_departments(db = Depends(get_db)):
    return db_queries.get_departments(db)

"""
Функция получает все должности из базы данных
    Параметры: db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: list[Position] — список должностей
"""
@app.get("/positions", response_model = List[Position])
def read_positions(db = Depends(get_db)):
    return db_queries.get_positions(db)

"""
Функция получает сотрудников из базы данных с возможной фильтрацией
    Параметры:
        department_id: int | None — id отдела 
        position_id: int | None — id должности 
        hire_date_from: str | None — дата начала найма 
        hire_date_to: str | None — дата конца найма
        db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: list[Employee] — список сотрудников
"""
@app.get("/employees", response_model = List[Employee])
def read_employees(department_id: int = None, position_id: int = None, hire_date_from: str = None, 
                   hire_date_to: str = None, db = Depends(get_db)):
    return db_queries.get_employees(db, department_id, position_id, hire_date_from, hire_date_to)


"""
Функция получает историю зарплат сотрудника по его id
    Параметры:
        employee_id: int — id сотрудника
        db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: list[SalaryHistory] — список записей о зарплате сотрудника
"""
@app.get("/salary/{employee_id}", response_model = List[SalaryHistory])
def read_salary(employee_id: int, db = Depends(get_db)):
    return db_queries.get_salary_history(db, employee_id)


"""
Функция создаёт нового сотрудника и добавляет начальную запись о зарплате
    Параметры:
        emp: EmployeeCreate — данные нового сотрудника
        db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: dict — информация о созданном сотруднике с текущей зарплатой
"""
@app.post("/employees", response_model = Employee)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = EmployeeModel(    # Создаём объект сотрудника SQLAlchemy
        last_name = emp.last_name,  # Фамилия сотрудника
        first_name = emp.first_name,  # Имя сотрудника
        middle_name = emp.middle_name,  # Отчество сотрудника 
        hire_date = emp.hire_date,  # Дата найма
        department_id = emp.department_id,  # id отдела
        position_id = emp.position_id  # id должности
    )
    db.add(new_emp)  # Добавляем сотрудника в сессию
    db.commit()  # Сохраняем изменения в базе
    db.refresh(new_emp)  # Обновляем объект после сохранения

     # Создание начальной записи зарплаты
    if emp.amount is not None:
        salary_record = SalaryHistoryModel(  # Объект истории зарплаты
            employee_id = new_emp.id,  # id сотрудника
            change_date = emp.hire_date,  # Дата начала зарплаты
            amount = emp.amount  # Сумма зарплаты
        )
        db.add(salary_record)  # Добавляем запись истории зарплаты
        db.commit()  # Сохраняем изменения
        db.refresh(salary_record)   # Обновляем объект

    # Вычисляем текущую зарплату
    salary_records = db.query(SalaryHistoryModel).filter(SalaryHistoryModel.employee_id == new_emp.id).order_by(SalaryHistoryModel.change_date.desc()).all()
    
    if salary_records:
        latest_date = salary_records[0].change_date # Берём дату последнего изменения зарплаты

        # Собираем все суммы зарплаты, которые относятся к самой последней дате
        latest_records = [r.amount for r in salary_records if r.change_date == latest_date]

         # Берём максимальную зарплату среди записей с одинаковой датой
        current_salary = max(latest_records)
    else:    
        current_salary = None # Если записей изменения зарплаты нет — текущей зарплаты тоже нет


    # Преобразуем объект в словарь
    result = {
        "id": new_emp.id,
        "last_name": new_emp.last_name,
        "first_name": new_emp.first_name,
        "middle_name": new_emp.middle_name,
        "hire_date": new_emp.hire_date,
        "department": {"id": new_emp.department.id, "name": new_emp.department.name},
        "position": {"id": new_emp.position.id, "name": new_emp.position.name},
        "current_salary": current_salary
    }

    return result



"""
Функция получает всех сотрудников с полной информацией
    Параметры: db: Session
    Возвращаемое значение: list[EmployeeFull] — список сотрудников с полной информацией
"""
@app.get("/employees/full", response_model = List[EmployeeFull])  
def get_employees_full(db=Depends(get_db)):
    employees = db.query(EmployeeModel).all()  # Получаем всех сотрудников из базы данных
    result = []  # Список для хранения результатов

    for emp in employees:  # Проходим по каждому сотруднику
        current_salary = None  # Инициализируем текущую зарплату
        if emp.salary_history:  # Если есть записи истории зарплаты
            # Находим максимальную дату изменения зарплаты
            latest_date = max(s.change_date for s in emp.salary_history)

            # Получаем ВСЕ суммы, у которых дата совпадает с самой последней
            salaries_on_latest_date = [s.amount for s in emp.salary_history if s.change_date == latest_date]

            # Выбираем максимальную сумму среди этих записей
            current_salary = max(salaries_on_latest_date)
        elif hasattr(emp, "amount") and emp.amount is not None:  # Если истории нет, но при создании была задана зарплата
            current_salary = emp.amount 
            
            # Создаём первую запись в истории зарплат (на дату найма)
            new_record = SalaryHistoryModel(employee_id = emp.id, change_date = emp.hire_date, amount = emp.amount)
            db.add(new_record)   # Добавляем запись в сессию
            db.commit() # Сохраняем изменения в базе данных
            db.refresh(new_record)   # Обновляем объект

        emp_data = EmployeeFull(  # Создаём объект EmployeeFull
            id = emp.id,  # id сотрудника
            last_name = emp.last_name,  # Фамилия
            first_name = emp.first_name,  # Имя
            middle_name = emp.middle_name,  # Отчество
            hire_date = emp.hire_date,  # Дата найма
            department = emp.department.name if emp.department else None,  # Название отдела (если есть)
            position = emp.position.name if emp.position else None,  # Название должности (если есть)
            current_salary = current_salary  # Текущая зарплата
        )
        result.append(emp_data)  # Добавляем объект в список результатов

    return result   


"""
Функция создаёт новый отдел
    Параметры: 
        dep: Department — данные нового отдела
        db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: Department — созданный отдел
"""
@app.post("/departments", response_model = Department)
def create_department(dep: Department, db: Session = Depends(get_db)):
    existing = db.query(DepartmentModel).filter(DepartmentModel.name == dep.name).first()      # Ищем отдел с таким же именем
    if existing:
        raise HTTPException(status_code = 400, detail = "Отдел с таким именем уже существует")
    new_dep = DepartmentModel(name = dep.name)     # Создаём объект модели SQLAlchemy
   
    db.add(new_dep)  # Добавляем объект в сессию БД
   
    db.commit()  # Сохраняем изменения
   
    db.refresh(new_dep)  # Обновляем объект, чтобы получить id, созданный БД
    return new_dep


"""
Функция создаёт новую должность
    Параметры: 
        pos: Position — данные создаваемой должности
        db: Session — объект сессии SQLAlchemy
    Возвращаемое значение: Position — созданная должность
"""
@app.post("/positions", response_model = Position)
def create_position(pos: Position, db: Session = Depends(get_db)):
    existing = db.query(PositionModel).filter(PositionModel.name == pos.name).first()    # Ищем должность с таким же именем
    if existing:
        raise HTTPException(status_code = 400, detail = "Должность с таким именем уже существует")
    new_pos = PositionModel(name = pos.name)
   
    db.add(new_pos)  # Добавляем запись в сессию
   
    db.commit()  # Фиксируем изменения
   
    db.refresh(new_pos)  # Обновляем объект, чтобы получить id, созданный БД
    return new_pos


"""
Функция добавляет запись в историю зарплат сотрудника
    Параметры: employee_id: int, sal: SalaryHistoryBase, db: Session
    Возвращаемое значение: SalaryHistory — созданная запись истории зарплаты
"""
@app.post("/salary/{employee_id}", response_model=SalaryHistory)
def add_salary_record(employee_id: int, sal: SalaryHistoryBase, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()  # Проверяем, что сотрудник существует
    if not employee:
        raise HTTPException(404, "Сотрудник не найден")

    new_record = SalaryHistoryModel(  # Создаём новый объект истории зарплаты
        employee_id = employee_id,  # Привязываем запись к конкретному сотруднику
        change_date = sal.change_date,  # Дата изменения зарплаты
        amount = sal.amount  # Сумма зарплаты
    )

    db.add(new_record)  # Добавляем запись в БД
    db.commit()  # Сохраняем изменения
    db.refresh(new_record)  # Обновляем объект, чтобы получить id, созданный БД

    return new_record


"""
Функция получает историю зарплат для указанного сотрудника
    Параметры: employee_id: int, db: Session
    Возвращаемое значение: list[SalaryHistory] — список записей истории зарплаты
"""
@app.get("/salary/{employee_id}", response_model = List[SalaryHistory])
def get_salary_history(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()  # Проверяем, что сотрудник существует
    if not employee:
        raise HTTPException(404, "Сотрудник не найден")

    salary_records = db.query(SalaryHistoryModel).filter(SalaryHistoryModel.employee_id == employee_id).all()  # Получаем все записи истории зарплаты
    return salary_records