


FROM python:3.12

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock* /app/

RUN pip install --upgrade pip && pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .


ENV SECRET_KEY=
ENV CELERY_BROKER_URL=
ENV CELERY_BACKEND=

RUN mkdir -p /app/media


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8800"]


