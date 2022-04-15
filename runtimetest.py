import grpc
import time
import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-20, y=4, z=-20),
        max=Point(x=20, y=14, z=20)
    ),
    type=AIR
))

for i in range(1,20,2):
    client.spawnBlocks(Blocks(blocks=
        [
            # Spawn a flying machine
        # Lower layer
        Block(position=Point(x=i, y=5, z=1), type=PISTON, orientation=NORTH),
        Block(position=Point(x=i, y=5, z=0), type=SLIME, orientation=NORTH),
        Block(position=Point(x=i, y=5, z=-1), type=STICKY_PISTON, orientation=SOUTH),
        Block(position=Point(x=i, y=5, z=-2), type=PISTON, orientation=NORTH),
        Block(position=Point(x=i, y=5, z=-4), type=SLIME, orientation=NORTH),
        # Upper layer
        Block(position=Point(x=i, y=6, z=0), type=REDSTONE_BLOCK, orientation=NORTH),
        Block(position=Point(x=i, y=6, z=-4), type=REDSTONE_BLOCK, orientation=NORTH)
    ]))
    time.sleep(2)


blocks = client.readCube(Cube(
    min=Point(x=1, y=5, z=-4),
    max=Point(x=1, y=6, z=1)
))

# print(blocks)
