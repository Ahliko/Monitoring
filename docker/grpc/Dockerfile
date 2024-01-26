FROM python:3.11.7
LABEL authors="Ahliko, Guervus"

RUN pip install grpcio grpcio-tools colorlog fire protobuf psutil six termcolor

WORKDIR /app
COPY ./monit /app

ENTRYPOINT ["python", "server.py"]