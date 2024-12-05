from typing import Counter
from TSP import *
from Mecanismos import *
from Data import *
from Configuracion import Config
from colorama import Fore, Back, Style


N = Config.N
pivote = Config.pivote

# INDIVIDUO

class Individuo:

    # Genera un nuevo individuo al azar
    def __init__(self, fun_inic):   
        self.values = fun_inic()

    def getCosto(self):
        costo = 0
        for i in range(0,N+1):
            costo += C(self.values[i],self.values[i+1])

    def isValid(self):
        values = self.values
        if (len(values) == Config.N + 1):                                       # La cantidad elementos coincide con la cantidad de ciudades (+ 1 por repetición de pivote)
            if (values[0] == values[len(values)-1] == Config.pivote):           # El primer y último elemento coinciden con la ciudad pivote
                counter = Counter(values[1:len(values)-1])
                if all(count == 1 for count in counter.values()):               # El resto de los elementos estan presentes una y solo una vez
                    return True
        return False


# GENERACION

class Generacion:


    def __init__(self,previous_gen=None):
        
        self.individuals = []

        if previous_gen is None:
            Generacion.counter = 1
            for i in range(0,Config.T_poblacion):
                self.individuals.insert(i,Individuo(Config.M_inicializacion))    # generados al azar
        
        else:
            Generacion.counter += 1

        self.id = Generacion.counter
        #print("gen ",self.id)



    def display(self):
        for individual in self.individuals:
            if (individual.isValid()):
                print(Fore.GREEN,individual.values,Style.RESET_ALL)     # VERDE: La solución es válida
            else:
                print(Fore.RED,individual.values,Style.RESET_ALL)       # ROJO: La solución no es válida



        