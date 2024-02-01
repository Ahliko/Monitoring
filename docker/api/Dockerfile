FROM python:3.11.7
LABEL authors="Ahliko, Guervus"

RUN pip install flask colorlog fire psutil six termcolor grpcio grpcio-tools protobuf flasgger

WORKDIR /app

COPY ./api /app

RUN chown -R 5000:5000 /app

ENTRYPOINT ["python", "api.py"]