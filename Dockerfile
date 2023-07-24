FROM python:3.10-buster as app
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off

RUN apt-get update -y\
    && apt upgrade -y \
    && apt autoremove -y \
    && pip install --upgrade pip \
    && pip install uwsgi  \
    && useradd --user-group --system datapunt

RUN apt install -y \
    gdal-bin \
    libpq-dev \
    gcc

USER datapunt

COPY deploy deploy

WORKDIR /app

WORKDIR /app/src
COPY requirements.txt requirements.txt
COPY src .

USER root
RUN pip install -r requirements.txt
USER datapunt

RUN python manage.py collectstatic --no-input

CMD ["/deploy/docker-run.sh"]

FROM app as dev

COPY requirements_dev.txt requirements_dev.txt
USER root
RUN pip install -r requirements_dev.txt

USER datapunt
CMD ["python", "/app/src/manage.py", "runserver", "0.0.0.0:8000"]

FROM dev as tests

WORKDIR /app/tests
COPY tests .
COPY pyproject.toml /app/.

ENV COVERAGE_FILE=/tmp/.coverage
ENV PYTHONPATH=/app/src
ENV DJANGO_SETTINGS_MODULE=main.settings

WORKDIR /app/

CMD ["pytest"]
