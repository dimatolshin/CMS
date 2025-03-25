FROM python:3.12-slim

WORKDIR /app

COPY . /app


RUN pip install --upgrade pip setuptools

RUN pip install -r requirements.txt


CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && \
<<<<<<< HEAD
    uvicorn app.asgi:application --workers 5 --host 0.0.0.0 --port 8000" ]
=======
    uvicorn mysite.asgi:application --workers 5 --host 0.0.0.0 --port 8000 ]
>>>>>>> 96ed352d0d1b504956722a2aaccf5ab050f4277b
