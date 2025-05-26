FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY req.txt /app/

# Обновляем pip и устанавливаем зависимости за один слой
RUN pip install --upgrade pip && pip install -r req.txt

COPY . /app/

# Открываем порт 8000
EXPOSE 8000

# Запуск приложения uvicorn напрямую
CMD ["uvicorn", "main:house_app", "--host", "0.0.0.0", "--port", "8000"]
