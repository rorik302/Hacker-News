FROM python:3.9.1-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install -y libssl-dev gcc default-libmysqlclient-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

COPY . .

CMD /wait && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
