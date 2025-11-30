@echo off
title HRM Project

:: Запускаем FastAPI
start "" uvicorn HRM:app --reload

:: Открываем главную HTML страницу
echo FastAPI server is running: http://127.0.0.1:8000

:: Открываем Swagger UI
start http://127.0.0.1:8000/docs

:: Ждём запуска сервера
timeout /t 5 /nobreak

:: Открываем HTML файл
start "" index.html

pause