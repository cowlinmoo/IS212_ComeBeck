# Base stage - installs core dependencies for general use
FROM python:3.12-slim-bookworm AS base

# Bump this to invalidate docker layer cache
ENV CACHEUPDATE 20241030

# Set the container's working directory
WORKDIR /code

# Change the default shell to bash
SHELL ["/bin/bash", "-c"]

# Install OS dependencies
RUN apt-get update && apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.create false

# Copy essential project files
COPY poetry.lock pyproject.toml .flake8 pytest.ini ./

# Copy application and test code
COPY backend backend
COPY tests tests
COPY postgres/init.sql postgres/init.sql

# Install dependencies
RUN poetry install

# Expose port
EXPOSE 8080

# Default command (if running FastAPI app)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

# E2E stage - installs Playwright dependencies in addition to core dependencies
FROM base AS e2e

# Install Playwright dependencies
RUN poetry run playwright install-deps

# Install Playwright itself
RUN poetry run playwright install