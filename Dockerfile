FROM python:3.11-alpine

WORKDIR /app

COPY reqs.txt .

RUN pip install -r reqs.txt

COPY . .

EXPOSE 8000

RUN mkdir -p /app/db_data

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]