import grpc
import time

from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.core.problem import IntegerProblem
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.operator.mutation import IntegerPolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations

import minecraft_pb2_grpc
from minecraft_pb2 import *


class MCProblem(IntegerProblem):
    def __init__(self):
        super(MCProblem, self).__init__()
        self.number_of_variables = 20
        self.number_of_objectives = 2

        self.lower_bound = [0] * 20
        self.upper_bound = [100] * 20

        #self.channel = grpc.insecure_channel('localhost:5001')
        #self.client = minecraft_pb2_grpc.MinecraftServiceStub(self.channel)


    def evaluate(self, solution):
        self.clear_cube()

        block_info = solution.variables

        blocks = []
        for i in range(0, self.number_of_variables, 4):
            x = block_info[i]
            y = block_info[i+1]
            z = block_info[i+2]
            btype = block_info[i+3]
            mcblock = MCBlock(x, y, z, btype)

            blocks.append(mcblock.create_block())

        print(blocks)
        print("=====")

        #client.spawnBlocks(Blocks(blocks))
        solution.objectives[0] = x + y
        solution.objectives[1] = y + z

        time.sleep(1)


    def clear_cube(self):
        pass
        #self.client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
        #    cube=Cube(
        #        min=Point(x=-10, y=4, z=-10),
        #        max=Point(x=10, y=14, z=10)
        #    ),
        #    type=AIR
        #))


    def get_name(self):
        return "MCProblem"


class MCBlock():
    def __init__(self, x, y, z, btype):
        self.x = x
        self.y = y
        self.z = z
        self.btype = btype

    def create_block(self):
        return Block(position=Point(x=self.x, y=self.y, z=self.z),
                     type=self.btype, orientation=NORTH)


if __name__ == "__main__":
    problem = MCProblem()

    max_evals = 100
    algorithm = NSGAII(
        problem=problem,
        population_size=10,
        offspring_population_size=10,
        mutation=IntegerPolynomialMutation(1 / problem.number_of_variables),
        crossover=IntegerSBXCrossover(1),
        termination_criterion=StoppingByEvaluations(max_evals)
    )

    algorithm.run()











#blocks = client.readCube(Cube(
#    min=Point(x=1, y=5, z=-4),
#    max=Point(x=1, y=6, z=1)
#))

# print(blocks)
