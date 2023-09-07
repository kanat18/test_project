# Выбор базового образа с Python
FROM python:3.8-slim

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . /app

# Установка зависимостей
RUN pip install -r requirements.txt

# Запуск приложения
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

