FROM python:3.10.0
WORKDIR /code
RUN apt update && apt install -y ffmpeg
RUN pip install -U pip setuptools
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
ENTRYPOINT python main.py