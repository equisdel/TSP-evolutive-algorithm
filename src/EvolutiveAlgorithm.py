# it gathers all the parameters from configuration and it runs the simulation4

class EvolutiveAlgorithm:

    # when we change from page 3 (parameters) to page 4 (execution) we create this Evolutive Algorithm

    def __init__(self,instance,metadata):            # metadata is a dictionary

        """ PREFIX CONVENTION:
            const:  numerical values that set the initial conditions (integers normally)
            prob:   numerical values that are used as probabilities (floats from 0 to 1 normally)
            mec:    mechanisms that define the algorithm's behaviour
            data:   descriptors of the algorithm with no impact on its behaviour
        """
        # de qué otra manera podes flexibilizar la convergencia en la UI?

        # general
        self.instance = instance            # access to current instance of TSP

        # initial population
        self.const_population_size = 100    # population size: fixed amount of individuals  
        self.const_city_of_origin = 0       # city of origin: where the salesman starts, changes nothing
        self.mec_initialization = "random"  # defines how the first generation is produced (at random by default)

        # convergency related
        self.const_min_generations = 100    # lower bound to avoid early convergency
        self.const_max_generations = -1     # upper bound to avoid no convergency at all, can be avoided by being set to -1
        self.const_min_epsilon =            # convergency related

        # mechanisms that define the next generation
        self.mec_parent_selection = ""        # defines how the parents are selected for crossing
        self.mec_parent_crossing = ""         # defines how the new individuals are generated from the parents
        self.mec_individual_mutation = ""     # defines the mutations applied to some of the new individuals
        self.mec_individual_survival = ""     # defines the selection of survivors for the next generation

        # probabilities that define the next generation
        self.prob_crossing = 0.5
        self.prob_mutation = 0.5

        # analytics: description of the execution
        self.data_best_solution_gen = None  
            # generation:   best solution found for this instance in the current generation of the execution
        self.data_best_solution_exe = None
            # execution:    best solution found for this instance in all the execution
        self.data_best_solution_abs = instance.best_solution or None      
            # absolute:     best solution found for this instance (can be from literature or previous executions)


    def update_parameters(self, metadata):
        for key, value in metadata.items():
            if hasattr(self, key):  # Validate that the attribute exists
                setattr(self, key, value)
            else:
                print(f"Warning: Unknown parameter '{key}'")
        return None

    def run(self):

        min_gens = self.const_min_generations
        gen_counter = 0

        # primera generacion
        
        actual_gen = Generation(self.mec_initialization)

        while (gen_counter < min_gens):


            # registro de las mejores soluciones hasta el momento

            # seleccion de padres

            # cruzamiento

            # mutaciones

            # seleccion de sobrevivientes

            # obtencion de la nueva generacion y se repite el ciclo
            gen_counter += 1



