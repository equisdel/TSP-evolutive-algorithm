class Config:   

    # VALORES POR DEFECTO

    # Simulacion
    N = None            # Cantidad de ciudades: se extrae de data/p43.atsp
    pivote = 0

    # Poblacion
    #C_poblacion = 3     # cruces por generación
    T_poblacion = 100    # cantidad fija de individuos

    MIN_generaciones = 1000     # probar con más, es
    MIN_epsilon_conv = 1        # quizas menor, es sobre el fitness

    
    # Mecanismos: cruzamiento y mutacion
    M_inicializacion = 0       # Generación espontánea de individuos aleatorios
    M_cruzamiento = 0              # Obtención de nuevos individuos por cruzamiento de existentes
    M_mutacion = 0                 # Modificacion genética de individuos existentes

    