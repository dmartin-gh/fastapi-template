FROM python:3.10-alpine

ENV PATH="/root/.local/bin:${PATH}"

RUN apk update
RUN apk add bash curl openssl

RUN curl -sSL https://install.python-poetry.org/ | python -

WORKDIR /build
COPY alembic.ini pyproject.toml poetry.lock /build/
COPY migrations /build/migrations
COPY src /build/src

RUN poetry config virtualenvs.create false
RUN poetry install --only main

ENTRYPOINT ["/usr/local/bin/serve"]
