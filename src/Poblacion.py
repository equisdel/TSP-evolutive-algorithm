from typing import Counter
from colorama import Fore, Back, Style
from TSPInstance import TSPInstance
import random

# Individual

class Individual:

    # Genera un nuevo individuo al azar
    def __init__(self, generation, fun_inic,instance):
        self.generation = generation
        self.instance = instance
        self.values = fun_inic(self,instance)

    def mec_initialization_random(self,instance):
        values = []             # individuo <-> string de enteros
        print(instance.dimension)
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

    def isValid(self):
        values = self.values
        if (len(values) == self.instance.dimension + 1):                                       # La cantidad elementos coincide con la cantidad de ciudades (+ 1 por repetición de pivote)
            if (values[0] == values[len(values)-1] == self.generation.city_of_origin):           # El primer y último elemento coinciden con la ciudad pivote
                counter = Counter(values[1:len(values)-1])
                if all(count == 1 for count in counter.values()):               # El resto de los elementos estan presentes una y solo una vez
                    return True
        return False
    
    def display(self):
        if (self.isValid()):
            print(Fore.GREEN,self.values,Style.RESET_ALL)     # VERDE: La solución es válida
        else:
            print(Fore.RED,self.values,Style.RESET_ALL)       # ROJO: La solución no es válida


# GENERATION

class Generation:

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
            self.individuals.insert(i,Individual(self,Individual.mec_initialization_random,instance))    # generados al azar

        #self.id = Generacion.counter

    def getBest(self):
        best = None
        best_fitness = -1
        for individual in self.individuals:
            if (individual.getCost() > best_fitness):
                best = individual
                best_fitness = individual.getCost()
        return best, best_fitness

    def display(self):
        for individual in self.individuals:
            individual.display()



        