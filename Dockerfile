FROM python:3.11

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /usr/src/app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --without dev

COPY . .

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--loop=uvloop", "--port=5000"]
