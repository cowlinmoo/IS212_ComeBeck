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
COPY poetry.lock pyproject.toml ./

COPY backend backend
COPY tests tests
# Copy the .env file (assuming it's in the same directory as your Dockerfile)
COPY .env /code/.env

# Install all dependencies
RUN poetry install

# Open required ports
EXPOSE 8080

# Set the command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
