from sqlalchemy.orm import Session
from models import Department, Position, Employee, SalaryHistory
from datetime import date


def init_data(db: Session):

    # ---- Создание отделов ----
    departments = [
        Department(name="Отдел разработки"),
        Department(name="Отдел кадров"),
        Department(name="Бухгалтерия"),
    ]
    db.add_all(departments)
    db.commit()

    # ---- Создание должностей ----
    positions = [
        Position(name="Разработчик"),
        Position(name="Тестировщик"),
        Position(name="HR-специалист"),
        Position(name="Бухгалтер"),
        Position(name="Системный администратор"),
    ]
    db.add_all(positions)
    db.commit()

    # ---- Создание сотрудников ----
    employees = [
        Employee(
            first_name="Иван",
            last_name="Иванов",
            hire_date=date(2020, 5, 10),
            department_id=1,
            position_id=1,
        ),
        Employee(
            first_name="Пётр",
            last_name="Петров",
            hire_date=date(2021, 3, 15),
            department_id=1,
            position_id=2,
        ),
        Employee(
            first_name="Елена",
            last_name="Сидорова",
            hire_date=date(2019, 11, 1),
            department_id=2,
            position_id=3,
        ),
        Employee(
            first_name="Мария",
            last_name="Кузнецова",
            hire_date=date(2022, 6, 20),
            department_id=3,
            position_id=4,
        ),
        Employee(
            first_name="Алексей",
            last_name="Фёдоров",
            hire_date=date(2018, 2, 5),
            department_id=1,
            position_id=5,
        ),
    ]
    db.add_all(employees)
    db.commit()

    # ---- История зарплат ----
    salary_history = [
        SalaryHistory(employee_id=1, change_date=date(2020, 5, 10), amount=80000),
        SalaryHistory(employee_id=1, change_date=date(2022, 1, 1), amount=95000),

        SalaryHistory(employee_id=2, change_date=date(2021, 3, 15), amount=60000),
        SalaryHistory(employee_id=2, change_date=date(2023, 1, 1), amount=72000),

        SalaryHistory(employee_id=3, change_date=date(2019, 11, 1), amount=55000),
        SalaryHistory(employee_id=3, change_date=date(2022, 5, 10), amount=65000),

        SalaryHistory(employee_id=4, change_date=date(2022, 6, 20), amount=70000),

        SalaryHistory(employee_id=5, change_date=date(2018, 2, 5), amount=90000),
        SalaryHistory(employee_id=5, change_date=date(2021, 9, 1), amount=105000),
    ]
    db.add_all(salary_history)
    db.commit()

    print("Начальные данные успешно загружены!")
