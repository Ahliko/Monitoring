import grpc
import monit_pb2_grpc
from google.protobuf import empty_pb2

def run():
    channel = grpc.insecure_channel('10.1.1.10:50051')
    stub = monit_pb2_grpc.MonitServiceStub(channel)

    # Call the method Check
    stub.Check(empty_pb2.Empty())

    # Call the method GetLast
    response = stub.GetLast(empty_pb2.Empty())
    print("Result from GetLast: ", response.result_json)

if __name__ == '__main__':
    run()
