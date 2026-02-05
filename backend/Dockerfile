# BASE
FROM python:3.12-slim-bullseye AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYSETUP_PATH="/backend" \
    VENV_PATH="/backend/.venv"

# prepend venv to path
ENV PATH="$VENV_PATH/bin:$PATH"

# `builder-base`
FROM base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.30 /uv /uvx /bin/

WORKDIR $PYSETUP_PATH
COPY pyproject.toml uv.lock ./

# Create venv and install dependencies
RUN uv venv $VENV_PATH && \
    uv sync --frozen --no-dev --no-install-project

COPY . .


# `DEVELOPMENT`
FROM base AS development
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
COPY app ./app
COPY tests ./tests
COPY development ./development

RUN uv venv $VENV_PATH && \
    uv sync --frozen

EXPOSE 8000
CMD ["uvicorn", "app.main:init_app", "--host", "0.0.0.0", \
     "--port", "8000", "--reload", "--no-access-log", "--factory"]


# `PRODUCTION`
FROM base AS production
ENV FASTAPI_ENV=production

WORKDIR $PYSETUP_PATH

COPY --from=builder-base $PYSETUP_PATH/.venv ./.venv
COPY --from=builder-base $PYSETUP_PATH/app ./app

CMD ["gunicorn", "app.main:init_app()", "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:80"]
