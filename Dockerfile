FROM ubuntu

RUN apt-get -y install python3-pip

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["python3", "main.py"]
