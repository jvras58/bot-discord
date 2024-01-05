FROM python:3.11
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "bot/main.py"]
