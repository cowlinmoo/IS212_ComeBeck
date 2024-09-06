# Use the official Python 3.12.3 image
FROM python:3.12-slim-bookworm

# Set this to 1 to build container with dev packages
ARG DEVELOPMENT=0

# Set container username
ARG USERNAME=app-user

# Bump this to invalidate docker layer cache
ENV CACHEUPDATE 20240903

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
RUN if [ "${DEVELOPMENT}" = "1" ]; \
    then \
        poetry install; \
    else \
        poetry install --only main; \
    fi

COPY backend backend
COPY main.py .
COPY test_main.http .

# Install all dependencies
RUN poetry install

# Open required ports
EXPOSE 8080

# Set the command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
