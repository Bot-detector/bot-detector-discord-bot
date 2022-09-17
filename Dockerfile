FROM python:3.10-slim

ARG api_port
ENV UVICORN_PORT ${api_port}

ARG root_path
ENV UVICORN_ROOT_PATH ${root_path}

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /project
COPY . /project

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /project
USER appuser

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0"] 