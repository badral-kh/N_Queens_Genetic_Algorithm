import random
import heapq
import math
import numpy as np
from time import time
import pygame
from pygame import display

WIDTH = 640
HEIGHT = 800
BLACK = (0,0,0)
WHITE = (255,255,255)

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
                    #check if there are two queens on same column
                    if genotype[i] == genotype[j]:
                        #check if the board has walls
                        if self.contain_walls == True:
                            #increment number of conflict if there is no wall between queens on same column on the board
                            if self.wall_between_horizontal_queens(genotype,i,j) == False:
                                num_conflicts += 1
                        else:
                            #increment number of conflict if there is no wall on the board and two queens are on same column
                            num_conflicts += 1
                    #check if there are two queens on same diagonal
                    if abs(i-j) == abs(genotype[i] - genotype[j]):
                        #check if the board has walls
                        if self.contain_walls == True:
                            #increment number of conflict if there is no wall between queens on same diagonal on the board
                            if self.wall_between_diagonal_queens(genotype,i,j) == False:
                                num_conflicts += 1
                        else:
                            #increment number of conflict if there is no wall on the board and two queens are on same diagonal
                            num_conflicts += 1
            #increment number of conflicts if a queen and a wall are on the same square
            if self.contain_walls == True:
                if (genotype[i] * self.size + i) in self.walls:
                    num_wall_queen_conflict += 1
        
        return int((num_conflicts / 2) + num_wall_queen_conflict)

    def fitness(self,genotype):
        num_conflicts = self.conflicts(genotype)
        #if there are conflict, set the fitness to 1 / number of conflicts.
        if num_conflicts != 0:
            return 1 / num_conflicts
        #genotype's fitness is set to infinite if there are no conflicts
        return math.inf
    
    def genetic_operator(self, parent_genotype1, parent_genotype2):
        i = random.randint(1,self.size-1)
        return parent_genotype1[0:i] + parent_genotype2[i:]

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
                print("solution found")
                return genotype
            self.add_population(genotype,genotype_fitness)
        return False

    def cross_selection(self):
        half_index = int(self.size / 2)
        for _ in range(half_index):
            two_random_num = random.sample(range(0, half_index), 2)
            parent1 = self.population[two_random_num[0]][1]
            parent2 = self.population[two_random_num[1]][1]
            offspring = self.genetic_operator(parent1,parent2)
            mutated_offpsring = self.mutation(offspring)
            mutated_offspring_fitness = self.fitness(mutated_offpsring)

            if mutated_offspring_fitness == math.inf:
                print("solution found")
                return mutated_offpsring
            
            self.population.pop(0)
            self.add_population(mutated_offpsring,mutated_offspring_fitness)
        return False

    def solve(self):
        start = time()
        return_populate = self.populate(self.num_population)
        if return_populate != False:
            end = time()
            self.run_time = end-start
            self.solution = return_populate
            return

        
        while True:
            return_val = self.cross_selection()
            self.num_generation += 1
            if return_val != False:
                end = time()
                self.run_time = end-start
                self.solution = return_val
                return
            
    def print_board(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("N-Queens variant using Genetic Algorithm")
        clock = pygame.time.Clock()
        screen.fill(pygame.Color("white"))

        #print generation
        font = pygame.font.Font("freesansbold.ttf", 32)
        text1 = "Number of generation: " + str(self.num_generation)
        text1 = font.render(text1,True,BLACK)

        text2 = "Run time: " + str(round(self.run_time, 3)) + "s"
        text2 = font.render(text2,True,BLACK)

        if self.contain_walls == True:
            text3 = "Number of walls: " + str(len(self.walls))
            text3 = font.render(text3,True,BLACK)

        running = True
        while running:
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            self.draw_board(screen,self.size)
            screen.blit(text1,(20,660))
            screen.blit(text2,(20,695))
            if self.contain_walls == True:
                screen.blit(text3,(20,730))
            clock.tick(15)
            pygame.display.flip()
        pygame.quit()

    def draw_board(self,screen, dimension):
        image = pygame.image.load("bQ.png")
        colors = [pygame.Color("white"), pygame.Color("light green")]
        sq_size = WIDTH // dimension
        image = pygame.transform.scale(image,(sq_size,sq_size))
        
        for r in range(dimension):
            for c in range(dimension):
                color = colors[((r+c) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
                if self.contain_walls == True:
                    if (r * self.size + c) in self.walls:
                        pygame.draw.rect(screen, pygame.Color("Black"), pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
                if self.solution[c] == r:
                    pygame.draw.rect(screen, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
                    screen.blit(image, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
                

chess = GeneticAlgorithm(50,50,800)

# chess = GeneticAlgorithm(8,40,0)

# chess = GeneticAlgorithm(8,40,5)

chess.solve()
chess.print_board()
 
# print(chess.run_time)
