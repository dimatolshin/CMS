FROM python:3.12-slim

WORKDIR /app

COPY . /app


RUN pip install --upgrade pip setuptools

RUN pip install -r requirements.txt


CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && \
    uvicorn mysite.asgi:application --workers 5 --host 0.0.0.0 --port 8000" ]
