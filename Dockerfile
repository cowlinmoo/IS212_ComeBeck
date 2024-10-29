# Use the official Python 3.12.3 image
FROM python:3.12-slim-bookworm

# Bump this to invalidate docker layer cache
ENV CACHEUPDATE 20240906

# Set the container's working directory
WORKDIR /code

# Change the default shell to bash
SHELL ["/bin/bash", "-c"]

# Install OS dependencies
RUN apt-get update \
    && apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.create false

# Copy the project files
COPY poetry.lock pyproject.toml .flake8 ./

COPY backend backend
COPY tests tests
COPY postgres/init.sql postgres/init.sql

# Install all dependencies
RUN poetry install

# Install Playwright OS dependencies
RUN poetry run playwright install-deps

# Install playwright
RUN poetry run playwright install

# Open required ports
EXPOSE 8080

# Set the command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
