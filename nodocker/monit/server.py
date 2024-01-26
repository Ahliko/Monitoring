#! /usr/bin/env python
from concurrent import futures

import grpc
from google.protobuf import empty_pb2

import monit_pb2
import monit_pb2_grpc
from monit import Monitoring


class MonitServiceServicer(monit_pb2_grpc.MonitServiceServicer):
    def Check(self, request, context):
        Monitoring().check()
        return empty_pb2.Empty()

    def GetLast(self, request, context):
        result = Monitoring().get("last")
        return monit_pb2.GetLastResponse(result_json=result)

    def List(self, request, context):
        result = Monitoring().list()
        return monit_pb2.ListResponse(items=result)

    def GetAvg(self, request, context):
        result = Monitoring().get("avg", request.parameter)
        return monit_pb2.GetAvgResponse(result_json=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    monit_pb2_grpc.add_MonitServiceServicer_to_server(MonitServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Starting server on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
