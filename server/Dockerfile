FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./alembic.ini ./

RUN uv sync --frozen --no-dev --no-install-project

COPY ./src/ ./src/

CMD ["uv", "run", "server"]
