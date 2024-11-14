FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN pip install poetry
RUN poetry install

COPY . /code/

CMD ["poetry", "run", "python", "browse_test/main.py"]
