FROM python:3.10-slim

ENV DAGSTER_HOME=/dagster_nyt_books/dagster_nyt_books

COPY dagster_nyt_books /dagster_nyt_books
COPY dbt_nyt_books /dagster_nyt_books/dagster_nyt_books/dbt_nyt_books
COPY dagster_nyt_books/dagster.yaml ${DAGSTER_HOME}
COPY dagster_nyt_books/workspace.yaml ${DAGSTER_HOME}

WORKDIR /dagster_nyt_books

RUN pip install .

WORKDIR /dagster_nyt_books/dagster_nyt_books/dbt_nyt_books

RUN dbt deps

EXPOSE 3000

WORKDIR ${DAGSTER_HOME}

