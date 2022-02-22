
from pickletools import pyfrozenset
import grpc
import controls_pb2 as cpb2
import controls_pb2_grpc
import math
import time

WAVEFRONTPARAMS = ["v", "vt", "vn", "vp", "f"]


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = controls_pb2_grpc.DroneControlStub(channel)
    response = stub.GetDroneInfo(cpb2.GetAllDroneRequest())
    nodes = response.nodes
    cnt = 0
    fd = open("lowpolytree.obj", "r")
    for line in fd:
        curr = line.split()
        if curr[0] in WAVEFRONTPARAMS:
            if curr[0] == "v":
#             rotating the object by 90 degrees on the y axis, scaling by 10 and then translating by 50 +z to get side view of the tree
#             using matrix
#               [ -sin(theta)*10 cos(theta)*10 0 0]
#               [ 0 0 10 0]
#               [ cos(theta)*10 sin(theta)*10 50 0]
#               [ 0 0 0 1]
#               theta is 90 in this case so sin = 1 and cos = 0
                x = -float(curr[1]) * 10
                y = (float(curr[3])) * 10 
                z = float(curr[2]) * 10 + 50
                nodes[cnt].posX = x
                nodes[cnt].posY = y
                nodes[cnt].posZ = z
                cnt = cnt + 1
    fd.close()
    theta = math.pi / 15
    while(True):
        for i in range(cnt):
            if i >= 117:
                response = stub.DroneUpdate(cpb2.DroneUpdateCommand(
                    id = nodes[i].id,
                    posx = nodes[i].posX, posy = nodes[i].posY, posz = nodes[i].posZ,
                    r = 87/255, g = 45/255, b = 16/255,a = nodes[i].a
                ))
            else:
                response = stub.DroneUpdate(cpb2.DroneUpdateCommand(
                    id = nodes[i].id,
                    posx = nodes[i].posX, posy = nodes[i].posY, posz = nodes[i].posZ,
                    r = 31/255, g = 255/255, b = 57/255,a = nodes[i].a
                ))
#               rotating around z axis by
#               [ cos(theta) sin(theta)* 0 0]            
#               [ -sin(theta)* cos(theta)* 0 0]
#               [ 0 0 1 0]
#               [ 0 0 0 1]
            x = nodes[i].posX*math.cos(theta) + nodes[i].posY * math.sin(theta)
            y = -nodes[i].posX*math.sin(theta) + nodes[i].posY * math.cos(theta)
            nodes[i].posX = x
            nodes[i].posY = y
#       fastest update time without crashing
        time.sleep(125/1000)

if __name__ == '__main__':
    run()