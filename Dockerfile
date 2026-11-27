# FROM base image
FROM python:3.12-trixie

# COPY the `uv` binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /api

# COPY dependencies (2 files!)
COPY pyproject.toml uv.lock ./

# COPY the code
# COPY . .
COPY api api
COPY src src
# COPY pipeline.py pipeline.py
# COPY predict.py predict.py
COPY models models
COPY README.md README.md
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

# RUN install dependencies
# RUN uv sync --frozen --no-install-project

#to save our gcs model
# RUN mkdir models

# Add virtualenv executables to PATH
# ENV PATH="/.venv/bin:$PATH"
ENV UV_NO_DEV=1 \
    UV_FROZEN=1

RUN uv sync

# CMD launch the API web server
# CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0"]
CMD ["uv", "run", "uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8080"]
