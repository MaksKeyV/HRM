@echo off
title HRM Project

:: 1. Запускаем FastAPI
start "" uvicorn HRM:app --reload

echo FastAPI server is running: http://127.0.0.1:8000

:: 2. Ждём запуска сервера
timeout /t 2 >nul

:: 3. Открываем HTML файл
start "" index.html

pause