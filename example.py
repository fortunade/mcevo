import grpc
import time
import csv

from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.core.problem import IntegerProblem
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.operator.mutation import IntegerPolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations

import minecraft_pb2_grpc
from minecraft_pb2 import *

population = 40
bound = 8
z_spacing = 2
x_spacing = 2


class MCProblem(IntegerProblem):
    def __init__(self):
        super(MCProblem, self).__init__()
        self.number_of_variables = 600
        self.number_of_objectives = 1

        # limits of variable values
        self.lower_bound = [4] * self.number_of_variables
        self.upper_bound = [4+bound] * self.number_of_variables

        self.channel = grpc.insecure_channel('localhost:5001')
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(self.channel)

        self.x_displacement = 0
        self.z_displacement = 0
        self.next_generation = population

        self.clear_cube()


    def evaluate(self, solution):
        ##self.clear_cube()

        block_info = solution.variables

        blocks = []
        if self.next_generation == 0:
            self.z_displacement += bound+z_spacing
            self.next_generation = population
            self.x_displacement=0

        ys = []
        uni_count=[]
        for i in range(0, self.number_of_variables, 3):
            x = block_info[i] + self.x_displacement
            y = block_info[i+1]
            z = block_info[i+2] + self.z_displacement
            
            #btype = 68 
            btype = [68,198,91,58]
            #emerald block, sea lantern, gold block, diamond block.
            mcblock = MCBlock(x, y, z, btype[y%4])

            blocks.append(mcblock.create_block())
            #blocks.append(Block(position=Point(x=x,y=y,z=z),type=btype[y%4],orientation=NORTH))
            ys.append(y)
            uni_count.append((x,y,z))
        print(blocks)
        print("=====")

        self.client.spawnBlocks(Blocks(blocks=blocks)) #spawns every solution
        
        solution.objectives[0] = sum(ys)#/len(ys)
##        solution.objectives[1] = 1/len(set(uni_count))
##        solution.objectives[0] = 0.3*self.objective_normalize(4,4+bound,sum(ys))+ 3*self.objective_normalize(0,self.number_of_variables/3,1/len(set(uni_count)))

        self.x_displacement += (bound + x_spacing)
        
        self.next_generation -= 1

        #time.sleep(1)


    def objective_normalize(self, xmin,xmax, x):
        return ((x-xmin)/(xmax-xmin))
        
        
    def clear_cube(self):
        self.client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
            cube=Cube(
                min=Point(x=-1, y=4, z=-1),
                max=Point(x=500, y=20, z=600)
            ),
            type=AIR
        ))


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

    max_evals = 2000
    algorithm = NSGAII(
        problem=problem,
        population_size=population,
        offspring_population_size=population,
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
