import random
import math
import numpy as np
from time import time

from numpy.random.mtrand import rand

class GeneticAlgorithm():

    def __init__(self,n,num_population,wall_count = 0):
        self.size = n
        self.population = []
        self.num_population = num_population
        self.solution = []
        self.num_generation = 1
        if wall_count != 0:
            self.contain_walls = True
            self.spawn_walls(wall_count)
        else:
            self.contain_walls = False

    def spawn_walls(self,wall_count):
        num_walls = wall_count
        self.walls = random.sample(range(0, self.size * self.size), num_walls)

    def wall_between_horizontal_queens(self, genotype, i, j):
        i_pos = genotype[i] * self.size + i
        j_pos = genotype[j] * self.size + j
        for wall_pos in self.walls:
            if wall_pos > i_pos and wall_pos < j_pos:
                return True
        return False
    
    def wall_between_diagonal_queens(self, genotype, i, j):
        i_pos = genotype[i] * self.size + i
        j_pos = genotype[j] * self.size + j

        num_squares_between_diagonal_Qs = abs(i-j) - 1
        if num_squares_between_diagonal_Qs == 0:
            return False
        
        if i < j and genotype[i] < genotype[j]:
            skip_index = self.size + 1
        elif i > j and genotype[i] > genotype[j]:
            skip_index = 0 - (self.size + 1)
        elif i < j and genotype[i] > genotype[j]:
            skip_index = 0 - (self.size - 1)
        elif i > j and genotype[i] < genotype[j]:
            skip_index = self.size - 1

        for i in range(i_pos + skip_index, j_pos, skip_index):
            if i in self.walls:
                return True
        return False

    def conflicts(self,genotype):
        num_conflicts = 0
        num_wall_queen_conflict = 0
        #iterate through each pair of columns in a genotype
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    if genotype[i] == genotype[j]:
                        if self.contain_walls == True:
                            if self.wall_between_horizontal_queens(genotype,i,j) == False:
                                num_conflicts += 1
                        else:
                            num_conflicts += 1
                    if abs(i-j) == abs(genotype[i] - genotype[j]):
                        if self.contain_walls == True:
                            if self.wall_between_diagonal_queens(genotype,i,j) == False:
                                num_conflicts += 1
                        else:
                            num_conflicts += 1
            if self.contain_walls == True:
                if (genotype[i] * self.size + i) in self.walls:
                    num_wall_queen_conflict += 1
            
        return int((num_conflicts / 2) + num_wall_queen_conflict)

    def fitness(self,genotype):
        num_conflicts = self.conflicts(genotype)
        if num_conflicts != 0:
            return 1 / num_conflicts
        return math.inf
    
    def genetic_operator(self, parent_genotype1, parent_genotype2):
        i = random.randint(1,self.size-1)
        if random.randint(0,10) < 5:
            return parent_genotype1[0:i] + parent_genotype2[i:]
        else:
            return parent_genotype2[0:i] + parent_genotype1[i:]

    def mutation(self,genotype):
        j = random.randint(0,self.size-1)
        z = random.randint(0,self.size-1)
        genotype[j] = z
        return genotype

    def add_population(self,genotyoe, genotype_fitness):
        for i in range(len(self.population)):
            if genotype_fitness < self.population[i][0]:
                self.population.insert(i,(genotype_fitness,genotyoe))
                return
        self.population.append((genotype_fitness,genotyoe))
        return
        
    def populate(self, num_population):

        for _ in range(num_population):
            #generate random genotype of size self.size from 0 to self.size - 1
            genotype = list(np.random.randint(low = self.size,size=self.size))
            genotype_fitness = self.fitness(genotype)
            if genotype_fitness == math.inf:
                return genotype
            self.add_population(genotype,genotype_fitness)
        return False

    def cross_selection(self):
        
        half_index = math.floor(self.size / 2)
        for _ in range(half_index):
            two_random_num = random.sample(range(0, half_index), 2)
            parent1 = self.population[two_random_num[0]][1]
            parent2 = self.population[two_random_num[1]][1]
            offspring = self.genetic_operator(parent1,parent2)
            mutated_offpsring = self.mutation(offspring)
            mutated_offspring_fitness = self.fitness(mutated_offpsring)

            if mutated_offspring_fitness == math.inf:
                return mutated_offpsring
            
            self.population.pop(0)
            self.add_population(mutated_offpsring,mutated_offspring_fitness)
        return False

    def solve(self):
        start = time()
        return_populate = self.populate(self.num_population)
        if return_populate != False:
            end = time()
            self.run_time = end - start
            self.solution = return_populate
            return

        while True:
            return_val = self.cross_selection()
            self.num_generation += 1
            if return_val != False:
                end = time()
                self.run_time = end - start
                self.solution = return_val
                return

    def print_solution(self):
        print("")
        for row in range(self.size):
            for col in range(self.size):
                print("|", end="")
                if self.solution[col] == row:
                    print("Q", end="")
                elif self.contain_walls == True:
                    if (row * self.size + col) in self.walls:
                        print("*", end="")
                    else:
                        print(" ",end="")
                else:
                    print(" ", end="")
            print("|")
        print("")


def main():
    total_run = 100
    total_time = 0
    total_generation = 0
    for i in range(total_run):
        chess = GeneticAlgorithm(16,16,112)
        chess.solve()
        chess.print_solution()
        total_time += chess.run_time
        total_generation += chess.num_generation
    
    print("Average time taken: " + str(round(total_time / total_run, 4)) + "s")
    print("Average number of generation: " + str(round(total_generation / total_run,2)))

    # print(chess.walls)

    # print("Runtime: " + str(round(chess.run_time,2)) + "s")
    # print("Number of generation: " + str(chess.num_generation))

if __name__ == "__main__":
    main()