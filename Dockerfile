FROM python:3.10-slim

WORKDIR /project
COPY ./requirements.txt /project/requirements.txt

RUN pip install --no-cache-dir -r /project/requirements.txt

COPY . /project/

CMD ["python","main.py" ]