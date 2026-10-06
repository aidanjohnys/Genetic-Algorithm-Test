import random
from time import sleep
import copy


class Individual:
    CHROMOSOME_SIZE = 16
    CHANCE_OF_MUTATION = 0.01

    def __init__(self, parent1_chromosome=None, parent2_chromosome=None):
        if parent1_chromosome is not None:
            self.chromosome = copy.deepcopy(parent1_chromosome[:self.CHROMOSOME_SIZE // 2])
            self.chromosome.extend(parent2_chromosome[:self.CHROMOSOME_SIZE // 2])

        else:
            self.chromosome = [0 for _ in range(self.CHROMOSOME_SIZE)]

            for i in range(len(self.chromosome)):
                if random.random() >= 0.5:
                    self.chromosome[i] = 1

    def fitness(self):
        return sum(self.chromosome) / self.CHROMOSOME_SIZE

    def mutate(self):
        for i in range(len(self.chromosome)):
            if random.random() <= self.CHANCE_OF_MUTATION:
                self.chromosome[i] ^= 1


class Simulation:
    INITIAL_POPULATION_SIZE = 50

    def __init__(self):
        self.population = [Individual() for _ in range(self.INITIAL_POPULATION_SIZE)]
        self.generation = 0

    def run(self):
        while self.population_fitness() < 0.90 and self.generation < 500:
            print(f"Generation: {self.generation}\n"
                  f"Fitness: {self.population_fitness():<10.02f}"
                  f"\nBest:   {self.best_individual().chromosome}, {self.best_individual().fitness():.02f}"
                  f"\nMedian: {self.median_individual().chromosome}, {self.median_individual().fitness():.02f}"
                  f"\nWorst:  {self.worst_individual().chromosome}, {self.worst_individual().fitness():.02f}\n")
            self.tournament_selection()
            random.shuffle(self.population)
            self.breed_population()
            self.mutate_population()
            self.generation += 1
            sleep(1)

    def tournament_selection(self):
        new_population = []

        for i in range(0, len(self.population), 2):
            if i + 1 >= len(self.population):
                winner = self.population[i]
            elif self.population[i].fitness() > self.population[i + 1].fitness():
                winner = self.population[i]
            else:
                winner = self.population[i + 1]

            new_population.append(winner)

        self.population = new_population

    def population_fitness(self):
        fitness = 0
        for i in range(len(self.population)):
            fitness += self.population[i].fitness()

        return fitness / float(len(self.population))

    def best_individual(self):
        best_individual = self.population[0]

        for i in range(1, len(self.population)):
            if self.population[i].fitness() > best_individual.fitness():
                best_individual = self.population[i]

        return best_individual

    def median_individual(self):
        return sorted(self.population, key=lambda x: x.fitness())[len(self.population) // 2]

    def worst_individual(self):
        worst_individual = self.population[0]

        for i in range(1, len(self.population)):
            if self.population[i].fitness() < worst_individual.fitness():
                worst_individual = self.population[i]

        return worst_individual

    def breed_population(self):
        for i in range(len(self.population)):
            parent1 = self.population[i]
            parent2 = self.population[i + 1]
            child = Individual(parent1.chromosome, parent2.chromosome)
            self.population.append(child)

    def mutate_population(self):
        for i in range(len(self.population)):
            self.population[i].mutate()


simulation = Simulation()
simulation.run()

