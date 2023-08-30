FROM python:3.11-slim-buster

WORKDIR /app
RUN mkdir data

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.py ./

ENTRYPOINT ["python3", "main.py"]