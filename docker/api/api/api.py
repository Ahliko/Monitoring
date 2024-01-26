import json
from logging import DEBUG

import colorlog
import grpc
from flask import Flask
from google.protobuf import empty_pb2

import monit_pb2_grpc

app = Flask(__name__)


logger = colorlog.getLogger()
logger.setLevel(DEBUG)
stream_handler = colorlog.StreamHandler()
stream_handler.setLevel(DEBUG)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "white",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


@app.route("/list")
def list():
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.List(empty_pb2.Empty())
    return response.items


@app.route("/getlast", methods=["GET"])
def getlast():
    """

    :return:
    """
    logger.debug("Debut getlast")
    with open("/etc/monit/config.json", encoding="utf-8") as file:
        file = file.read()
        grpc_port = json.loads(file)["GRPC_PORT"]
        grpc_host = json.loads(file)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.GetLast(empty_pb2.Empty())
    logger.debug("Fin getlast")
    return response.result_json


@app.route("/getavg")
def getavg():
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.GetAvg(empty_pb2.Empty())
    return response.result_json


@app.route("/check")
def check():
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    stub.Check(empty_pb2.Empty())
    return "OK"


if __name__ == "__main__":
    port = json.load(open("/etc/monit/config.json"))["PORT"]
    host = json.load(open("/etc/monit/config.json"))["HOST"]
    app.run(host=host, port=port, debug=True)
