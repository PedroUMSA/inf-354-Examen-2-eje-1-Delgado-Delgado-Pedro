import random
import string
import numpy as np
import pandas as pd
from deap import base, creator, tools


class Generaciones:
    def __init__(self, toolbox):
        self.toolbox = toolbox
        self.set_parameters(10, 5, 2)
        
    def set_parameters(self, size_poblacion, iterations, nro_pares):
        self.iterations = iterations
        self.size_poblacion = size_poblacion
        self.nro_pares = nro_pares
        
    def set_fitness(self, population):
        fitnesses = [ 
            (individual, self.toolbox.evaluar(individual)) 
            for individual in population 
        ]

        for individual, fitness in fitnesses:
            individual.fitness.values = (fitness,)
            
    def get_offspring(self, population):
        n = len(population)
        for _ in range(self.nro_pares):
            i1, i2 = np.random.choice(range(n), size=2, replace=False)

            offspring1, offspring2 = \
                self.toolbox.mate(population[i1], population[i2])
            
            yield self.toolbox.mutate(offspring1)[0]
            yield self.toolbox.mutate(offspring2)[0]
    
    def pull_stats(population, iteration=1):
        fitnesses = [ individual.fitness.values[0] for individual in population ]
        return {
            'Generacion': iteration,
            'media': np.mean(fitnesses),
            'Desviacion estandar': np.std(fitnesses),
            'Maximo': np.max(fitnesses),
            'Minimo': np.min(fitnesses),
            'poblacion':population,
        }  
    
    def generar(self):
        population = self.toolbox.population(n=self.size_poblacion)
        self.set_fitness(population)
        
        stats = []
        for iteration in list(range(1, self.iterations + 1)):
            current_population = list(map(self.toolbox.clone, population))
            offspring = list(self.get_offspring(current_population))            
            for child in offspring:
                current_population.append(child)
            
            ## reset fitness,
            self.set_fitness(current_population)
            
            population[:] = self.toolbox.select(current_population, len(population))
            stats.append(
                Generaciones.pull_stats(population, iteration))
            
        return stats, population

def evaluar(individual):
    summation = 0
    start = individual[0]
    for i in range(1, len(individual)):
        end = individual[i]
        summation += distances[start][end]
        start = end
    init= distances[end][individual[0]]
    return summation+init

#main
datos= pd.read_csv('datos.csv')

datos=datos.drop(datos.columns[datos.columns.str.contains('unnamed',case = False)],axis = 1)
distan= datos.iloc[:].values.tolist()
print(datos)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
random.seed(11);
np.random.seed(121);

size_individuo = 4
size_poblacion = 10
nro_ireraciones = 40
nro_pares = 5
prob_mutacion=0.5

distances = distan
toolbox = base.Toolbox()

#permutacion para los individuos
toolbox.register("indices", random.sample, range(size_individuo), size_individuo)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
#poblacion
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


toolbox.register("evaluar", evaluar)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=prob_mutacion)
toolbox.register("select", tools.selTournament, tournsize=10)

a = Generaciones(toolbox)
a.set_parameters(size_poblacion, nro_ireraciones, nro_pares)
stats, population = a.generar()

fitnesses = sorted([ (i, toolbox.evaluar(indi)) for i, indi in enumerate(population)
], key=lambda x: x[1])

for s in stats:
    print(s)
for pop in range(len(population)):
    print('Rutas# ',pop,' con total de: ',fitnesses[:][pop][1])
    for i in range(len(population[pop])):
        if population[pop][i]==0:
            print('Monoblock')
        if population[pop][i]==1:
            print('Ingeniera')
        if population[pop][i]==2:
            print('Derecho')
        if population[pop][i]==3:
            print('Cota Cota')
    print('\n')

