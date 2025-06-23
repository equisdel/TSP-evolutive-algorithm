from typing import Counter
from colorama import Fore, Back, Style
#from TSPInstance import TSPInstance
import random

# Individual

class Individual:

    instance = None
    # Genera un nuevo individuo al azar
    def __init__(self,generation, instance, fun_inic=None, values=None):
        self.generation = generation
        self.instance = instance
        self.values = fun_inic(self,instance) if fun_inic is not None else values

    def mec_initialization_random(self,instance):
        values = []             # individuo <-> string de enteros
        #print(instance.dimension)
        for i in range(0,instance.dimension):
            if (i!=self.generation.city_of_origin):
                values.insert(i,i)
        random.shuffle(values)
        values.insert(0, self.generation.city_of_origin)
        values.insert(instance.dimension, self.generation.city_of_origin)
        
        return values

    def getCost(self):
        cost = 0
        for i in range(0,self.instance.dimension):
            cost += self.instance.matrix[self.values[i],self.values[i+1]]
        return cost
    
    def getFitness(self):
        cost = self.getCost()
        fitness = -cost + Generation.max_cost
        return fitness

    def isValid(self):
        values = self.values
        if (len(values) == self.instance.dimension + 1):                                       # La cantidad elementos coincide con la cantidad de ciudades (+ 1 por repetición de pivote)
            if (values[0] == values[len(values)-1] == self.generation.city_of_origin):           # El primer y último elemento coinciden con la ciudad pivote
                counter = Counter(values[1:len(values)-1])
                if all(count == 1 for count in counter.values()):               # El resto de los elementos estan presentes una y solo una vez
                    return True
        return False
    
    def getValues(self):
        return self.values

    def display(self):
        if (self.isValid()):
            print(Fore.GREEN,self.values,Style.RESET_ALL,self.getCost())     # VERDE: La solución es válida
        else:
            print(Fore.RED,self.values,Style.RESET_ALL,self.getCost())       # ROJO: La solución no es válida


# GENERATION

class Generation:

    max_cost = 0
    max_cost_offset = 3     # avoids individuals having zero chance of getting laid

    def __init__(self,mec_initialization=None,previous_gen=None,population_size=0,instance_size=0,origin=0,instance=None):
        
        self.individuals = []   # eficiencia?
        self.city_of_origin = origin

        if (mec_initialization!=None):      # primera generación
        
            self.gen_id = 0
            method_name = f"mec_gen_initialization_{mec_initialization}"
            method = getattr(self, method_name, None)

            if callable(method):
                method(population_size,instance)
            else:
                print(f"Method '{method_name}' not found!")
            
        #else:
        #    Generacion.counter += 1

        #self.id = Generacion.counter
        #print("gen ",self.id)

    def mec_gen_initialization_random(self,population_size,instance):
        for i in range(0,population_size):
            new_individual = Individual(self,instance,fun_inic=Individual.mec_initialization_random)
            self.individuals.insert(i,new_individual)    # generados al azar
            if new_individual.getCost() > Generation.max_cost:
                Generation.max_cost = new_individual.getCost() + self.max_cost_offset

        #self.id = Generacion.counter

    def getIndividual(self,index):
        return self.individuals[index]
    
    def getIndividuals(self):
        return list(self.individuals)

    def getBest(self):
        best = None
        best_fitness = -1
        for individual in self.individuals:
            if (individual.getFitness() > best_fitness):
                best = individual
                best_fitness = individual.getFitness()
        return best, best_fitness
    
    def getFitnessList(self):
        fitness_list = []
        for i, individual in enumerate(self.individuals):
            fitness_list.append(individual.getFitness())
        return fitness_list

    def display(self):
        for individual in self.individuals:
            individual.display()



        