
from fastapi import FastAPI, Depends
from typing import List
from database import Base, engine, get_db, SessionLocal
import crud
from schemas import Employee, Department, Position, SalaryHistory
from dataHRM import init_data
from models import Employee as EmployeeModel  # чтобы проверить пусто ли

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Создание таблиц ----
Base.metadata.create_all(bind=engine)

# ---- Инициализация данных (один раз) ----
db = SessionLocal()
if not db.query(EmployeeModel).first():   # проверяем, есть ли хоть один сотрудник
    init_data(db)
db.close()



@app.get("/departments", response_model=List[Department])
def read_departments(db=Depends(get_db)):
    return crud.get_departments(db)


@app.get("/positions", response_model=List[Position])
def read_positions(db=Depends(get_db)):
    return crud.get_positions(db)


@app.get("/employees", response_model=List[Employee])
def read_employees(
    department_id: int = None,
    position_id: int = None,
    hire_date_from: str = None,
    hire_date_to: str = None,
    db=Depends(get_db),
):
    return crud.get_employees(db, department_id, position_id, hire_date_from, hire_date_to)


@app.get("/salary/{employee_id}", response_model=List[SalaryHistory])
def read_salary(employee_id: int, db=Depends(get_db)):
    return crud.get_salary_history(db, employee_id)
