from flask import Flask
import grpc
import monit_pb2_grpc
from google.protobuf import empty_pb2
import json

app = Flask(__name__)


@app.route("/list")
def list():
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.List(empty_pb2.Empty())
    return response.items


@app.route("/getlast")
def getlast():
    with open("/etc/monit/config.json") as f:
        grpc_port = json.load(f)["GRPC_PORT"]
        grpc_host = json.load(f)["GRPC_HOST"]
    channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
    stub = monit_pb2_grpc.MonitServiceStub(channel)
    response = stub.GetLast(empty_pb2.Empty())
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
