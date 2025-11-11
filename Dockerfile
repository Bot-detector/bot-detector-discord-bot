FROM python:3.12.10-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG api_port
ENV UVICORN_PORT ${api_port}

ARG root_path
ENV UVICORN_ROOT_PATH ${root_path}

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# set the working directory
WORKDIR /project

# install dependencies
COPY ./requirements.txt /project
# RUN pip install -r requirements.txt
COPY ./pyproject.toml /project
COPY ./uv.lock /project
RUN uv sync --locked --no-editable

# copy the scripts to the folder
COPY ./src /project/src

# production image 
FROM base AS production
# Creates a non-root user with an explicit UID and adds permission to access the /project folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /project
USER appuser

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0"]
