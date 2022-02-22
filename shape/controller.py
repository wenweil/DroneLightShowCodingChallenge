#todo: create framework to read stl files
#todo: stl to shape transform
#todo: rotation

import grpc
import controls_pb2 as cpb2
import controls_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = controls_pb2_grpc.DroneControlStub(channel)
        response = stub.DroneUpdate(cpb2.DroneUpdateCommand(id = "drone301",
                                posx = 10, posy = -70, posz = 25,
                                r = 1.0, g = 1.0, b = 1.0, a = 1.0))
    print(response)

if __name__ == '__main__':
    run()