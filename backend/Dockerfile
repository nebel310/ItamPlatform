# Используем официальный образ Python
FROM python:3.11.7-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь код приложения
COPY . .

# Открываем порт для приложения
EXPOSE 5001

# Команда для запуска приложения
CMD ["python", "app.py"]