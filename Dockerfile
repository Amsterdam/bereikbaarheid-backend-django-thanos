FROM python:3.11-slim-bullseye as app

WORKDIR /app

ENV PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off

RUN apt-get update -y\
    && apt upgrade -y \
    && apt autoremove -y

RUN apt install -y \
    gdal-bin \
    libpq-dev \
    gcc

COPY deploy deploy

WORKDIR /app/src
COPY requirements/requirements.txt requirements.txt
COPY src .

RUN pip install -r requirements.txt


CMD ["/deploy/docker-run.sh"]

FROM app as dev
COPY requirements/requirements_dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM dev as tests

WORKDIR /app/tests
COPY tests .
ENV COVERAGE_FILE=/tmp/.coverage
ENV PYTHONPATH=/app/src
ENV DJANGO_SETTINGS_MODULE=main.settings

WORKDIR /app/

CMD ["pytest"]
