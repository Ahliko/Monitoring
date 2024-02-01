import monit_pb2_grpc
from google.protobuf import empty_pb2
from flask import Flask
from flasgger import Swagger
import json
import grpc
from logging import DEBUG
import colorlog

app = Flask(__name__)
swag = Swagger(app)

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

# Endpoint for listing items
@app.route("/list", methods=["GET"])
def list_items():
    """
    List items.
    ---
    responses:
      200:
        description: A list of items.
    """
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.List(empty_pb2.Empty())
    return {"items": response.items}

# Endpoint for getting the last item
@app.route("/getlast", methods=["GET"])
def get_last():
    """
    Get the last item.
    ---
    responses:
      200:
        description: The last item.
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
    return {"result_json": response.result_json}

# Endpoint for getting average
@app.route("/getavg", methods=["GET"])
def get_average():
    """
    Get the average.
    ---
    responses:
      200:
        description: The average result.
    """
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.GetAvg(empty_pb2.Empty())
    return {"result_json": response.result_json}

# Endpoint for checking
@app.route("/check", methods=["GET"])
def check():
    """
    Check the service.
    ---
    responses:
      200:
        description: OK if the service is running.
    """
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
