import grpc
import time
import json

import minecraft_pb2_grpc
from minecraft_pb2 import *

class MCBlock():
    def __init__(self, x, y, z, btype):
        self.x = x
        self.y = y
        self.z = z
        self.btype = btype

    def create_block(self):
        return Block(position=Point(x=self.x, y=self.y, z=self.z),
                     type=self.btype, orientation=NORTH)


channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  #clear set area
    cube=Cube(
        min=Point(x=-1, y=4, z=-1),
        max=Point(x=500, y=20, z=600)
    ),
    type=AIR
))


blocklist_json = open('blocklist.json', mode='r')
jsonRead= blocklist_json.read()
blocklist=json.loads(jsonRead)


blocks = []

for i in range(len(blocklist['blocks'])):
    print(blocklist['blocks'][i])
##    info = {'x': 1, 'y': 4, 'z': 10, 'btype': 68}
    info = blocklist['blocks'][i]
    mcblock = MCBlock(info['x'], info['y'], info['z'], info['btype'])
    blocks.append(mcblock.create_block())

client.spawnBlocks(Blocks(blocks=blocks)) #spawns every solution
        
