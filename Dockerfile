FROM python:3.6

ADD requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ADD manage.py /app/manage.py
ADD pms /app/pms
ADD reservations /app/reservations

EXPOSE 8000
VOLUME /app/db

CMD gunicorn pms.wsgi:application --bind=0.0.0.0:8000
