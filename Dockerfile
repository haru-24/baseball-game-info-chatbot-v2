FROM python:3.12-slim-bookworm

ARG DEVELOPMENT=0


ENV UV_CACHE_DIR=/root/.cache/uv
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT='/usr/local/'
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app



# バージョンを指定してuvをコピー
COPY --from=ghcr.io/astral-sh/uv:0.5.27 /uv /bin/uv

# Install dependencies
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /app


CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=8000"]