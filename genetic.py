import numpy as np
import random

class Agent():
    def __init__(self, length):
        self.length = length
        self.value = np.random.choice([0, 1], size=(self.length,), p=[4/5, 1/5])
        self.fitness = -1
        
    def __str__(self):
        return 'Value: ' + str(self.value) + ' Fitness: ' + str(self.fitness) + '\n'

class Population():
    def __init__(self, pop_size, bits, pc, pm):
        self.pop_size = pop_size
        self.bits = bits
        self.pc = pc
        self.pm = pm
        self.population = [Agent(self.bits) for _ in range(self.pop_size)]
        self.newGeneration = []

         
    def __str__(self):
        string = ''
        for agent in self.population:
            string += 'Value: ' + str(agent.value) + ' Fitness: ' + str(agent.fitness) + '\n'
        return string
    
    def selection(self):
        # sort by best
        agents = sorted(self.population, key=lambda a: a.fitness, reverse=True)
        # total fitness
        total_fitness = sum(a.fitness for a in agents)
        # probs of each agent
        probs = [a.fitness/total_fitness for a in agents]
        # accumulative probs
        q_probs = np.cumsum(probs)
        
        # spin roullete pop_size times
        for _ in range(self.pop_size):
            # generate prob
            p = random.random()
            # find correct slot
            for j in range(self.pop_size):
                if p <= q_probs[j]:
                    self.newGeneration.append(agents[j])
                    break
        self.population = self.newGeneration[:]
        return self
    
    def crossover(self):    
        crossovers = []
        offspring = []
        
        for agent in self.population:
            # probability of cross over
            if random.random() <= self.pc:
                crossovers.append(agent)
        
        cross_len = len(crossovers)
        if cross_len > 1:
            for i in range(cross_len // 2):
                
                # random index to slice
                pt = random.randint(0, self.bits-1)
                
                # pick pairs
                bs1 = crossovers[i]
                bs2 = crossovers[i+1]
                
                if bs1 != bs2:
                    # create ancestors
                    child1 = Agent(self.bits)
                    child2 = Agent(self.bits)
                    
                    # give them the values
                    child1.value = np.concatenate((bs1.value[:pt], bs2.value[pt:]))
                    child2.value = np.concatenate((bs2.value[:pt], bs1.value[pt:]))
                    
                    # append offsprings
                    offspring.append(child1)
                    offspring.append(child2)
                    
            # remove parents
            for cro in crossovers:
                self.population.remove(cro)
                
            self.population.extend(offspring)
        
        return self
    
    def mutation(self):
        for agent in self.population:
            for i in range(self.bits):
                if random.random() <= self.pm:
                    agent.value[i] = 1 - agent.value[i]
        return self
    
    def validate_agent(self, agent):
        if agent.fitness >= 124:
            return True
        return False
            
    def find_best(self):
        index = 0
        for i in range(1, len(self.population)):
            if self.population[i].fitness > self.population[index].fitness:
                index = i
        return self.population[index]