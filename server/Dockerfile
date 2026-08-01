FROM python:3.14-slim

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY ./src/ ./src/

CMD ["uv", "run", "python", "-m", "src"]
