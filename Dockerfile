FROM python:3.9-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.1.14

RUN pip install --user poetry
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /opt/ml_service

COPY poetry.lock pyproject.toml /

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

CMD ["python", "main.py"]