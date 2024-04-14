# syntax=docker/dockerfile:1

FROM python:3.10.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt \
    && pip install djangorestframework \
    && pip install cloudinary \
    && pip install python-decouple

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
