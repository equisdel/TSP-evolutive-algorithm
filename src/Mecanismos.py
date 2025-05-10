"""import random
from TSP import *
#from Configuracion import Config

# INICIALIZACION DE INDIVIDUO

pivote = Config.pivote
cant_ciudades = Config.N

def inicializacion_al_azar():
    values = []             # individuo <-> string de enteros
    for i in range(0,cant_ciudades):
        if (i!=pivote):
            values.insert(i,i)
    random.shuffle(values)
    values.insert(0, pivote)
    values.insert(cant_ciudades, pivote)
    print(values)

# CRUZAMIENTO PARA OBTENCION DE NUEVOS INDIVIDUOS

def cruzamiento_simple(p1, p2):
    values = []
    return values

# MUTACION PARA MODIFICACION DE INDIVIDUOS EXISTENTES

def mutacion_ponderada(ind):
    values = ind.values
    return values
"""