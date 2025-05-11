"""import random
#from Configuracion import *
from Mecanismos import *
from Poblacion import Generacion
#from Data import *


# MUTACION PARA MODIFICACION DE INDIVIDUOS EXISTENTES

def inicializacion_al_azar():

    values = []             # individuo <-> string de enteros
    for i in range(0,Config.N):
        if (i!=pivote):
            values.insert(i,i)
    random.shuffle(values)
    values.insert(0, Config.pivote)
    values.insert(Config.N, Config.pivote)
    
    return values


# CRUZAMIENTO PARA OBTENCION DE NUEVOS INDIVIDUOS

def cruzamiento_simple(p1, p2):
    values = []
    return values


# MUTACION PARA MODIFICACION DE INDIVIDUOS EXISTENTES

def mutacion_ponderada(ind):
    values = ind.values
    return values


class TSP_simulation:

    def __init__(self):
        # opcion de retomar ejecucion anterior (pasado un archivo como parámetro)

        poblacion = Generacion()                    # primera generacion
        poblacion.display()
        iteracion = 0
        MIN_generaciones = Config.MIN_generaciones
        while (iteracion < MIN_generaciones-1):
            poblacion = Generacion(poblacion)     # La generación siguiente depende de la actual
            iteracion += 1

    # estadísticas, checkpoint


# MAIN
if __name__ == "__main__":
    
    Config()

    # PARAMETROS DE LA SIMULACION
    Config.MIN_generaciones = 1000                      # cantidad mínima de generaciones antes de converger
    Config.MIN_epsilon_conv = 0.01                      # epsilon de convergencia
    Config.pivote = 0                                   # ciudad de origen (es indistinto)

    # PARAMETROS DEL ALGORITMO
    Config.T_poblacion = 12                             # tamaño fijo de la población
    Config.M_inicializacion = inicializacion_al_azar    # 0 parámetros.
    Config.M_cruzamiento = cruzamiento_simple           # 2 parámetros: p1, p2.
    Config.M_mutacion = mutacion_ponderada              # 1 parámetro: ind.

    #Data("data\p43.atsp")                               # lectura del archivo data/p43.atsp

    TSP_simulation()                                    # SIMULACION

"""
