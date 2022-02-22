

from direct.showbase.ShowBase import ShowBase
from direct.stdpy.threading import Thread

from concurrent import futures

import grpc
import controls_pb2 as control
import controls_pb2_grpc

SWARM_ROWS = 20
SWARM_COLS = 15
swarm = dict()

class DroneControlServicer(controls_pb2_grpc.DroneControlServicer):
    def GetDroneInfo(self, request, context):
        ret = []
        for item in swarm.values():
            n = control.Node(id = item['id'],
                posX = item['posX'], posY = item['posY'], posZ = item['posZ'],
                r = item['r'], g = item['g'], b = item['b'], a = item['a'])
            ret.append(n)
        return control.DroneInfoReqResponse(nodes = ret)

    def DroneState(self, request, context):
        drone = request.id
        if drone in swarm:
            item = swarm[drone]
            n = control.Node(id = item['id'],
                posX = item['posX'], posY = item['posY'], posZ = item['posZ'],
                r = item['r'], g = item['g'], b = item['b'], a = item['a'])
            return control.DroneStateResponse(node = n)
        else:
            return control.GetAllDroneRequest()

    def DroneUpdate(self, request, context):
        drone = request.id
        if drone in swarm:
            item = swarm[drone]
            posX = request.posx
            posY = request.posy
            posZ = request.posz
            r = request.r
            g = request.b
            b = request.b
            a = request.a
            ref = item['ref']
            ref.setPos(posX,posY,posZ)
            ref.setColor(r,g,b,a)
            newItem = {
                    'id' : drone,
                    'posX' : posX, 'posY': posY, 'posZ': posZ,
                    'r': r, 'g': g, 'b':b, 'a': a,
                    'ref': ref
                }
            swarm[drone] = newItem
            return control.DroneUpdateResponse(success = True)
        else:
            return control.DroneUpdateResponse(success = False)


def serve():
    svr = grpc.server(futures.ThreadPoolExecutor(max_workers= 10))
    controls_pb2_grpc.add_DroneControlServicer_to_server(DroneControlServicer(),svr)
    svr.add_insecure_port('[::]:50051')
    print("svr starting...")
    svr.start()
    svr.wait_for_termination()
    
t = Thread(target=serve)
        

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0,-150,60)
        cnt = 1
        for i in range(SWARM_ROWS):
            for j in range(SWARM_COLS):
                b = self.loader.loadModel("models/box")
                b.setPos(-30+j*4,0+4*i,0)
                b.setColor(1.0,0.0,0.0,1.0)
                b.reparentTo(self.render)
                id = "drone"+str(cnt)
                tmp = {
                    'id' : id,
                    'posX' : -30+j*4, 'posY': 0+4*i, 'posZ': 0,
                    'r': 1.0, 'g': 0.0, 'b':0.0, 'a': 1.0,
                    'ref': b
                }
                swarm[id] = tmp
                cnt = cnt + 1
        t.start()
        
app = App()
app.run()        
t.join()
