
# Подключение к БД

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL подключения к базе данных MySQL
DATABASE_URL = "mysql+pymysql://root:sql2003@127.0.0.1:3306/hmr_work"

# Создаём объект подключения к базе данных
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping = True    # Проверяем соединение перед использованием, чтобы не было ошибок при простое
)

# Создаём шаблон для работы с базой 
SessionLocal = sessionmaker(
    autocommit = False, # Изменения не сохраняются сами, нужно подтвердить их вручную
    autoflush = False,  # Данные не отправляются в базу сразу, пока не сделан коммит
    bind = engine  # Привязываем сессию к нашему подключению к базе
)

# Основной шаблон для таблиц — все наши таблицы будут его использовать
Base = declarative_base()

"""
Функция создаёт сессию для работы с базой данных
    Параметры: отсутствуют
    Возвращаемое значение: объект сессии db, через который можно читать и изменять данные
"""
def get_db():
    db = SessionLocal() # Создаём новую сессию
    try:
        yield db    # Передаём сессию в обработчик FastAPI
    finally:
        db.close()   # Закрываем сессию, когда обработчик завершил работу