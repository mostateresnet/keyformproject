FROM python:3.7
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN mkdir /app
WORKDIR /app
COPY uv.lock pyproject.toml ./
RUN uv sync
CMD exec uv run uwsgi --ini keyformproject/keyform.ini
