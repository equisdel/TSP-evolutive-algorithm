# it gathers all the parameters from configuration and it runs the simulation4
from Population import Generation, Individual
from MecSelection import Selection
from MecCrossover import Crossover
from MecMutation import Mutation
# for test
from TSPInstance import TSPInstanceParser

class EvolutiveAlgorithm:

    # when we change from page 3 (parameters) to page 4 (execution) we create this Evolutive Algorithm

    def __init__(cls,instance,metadata):            # metadata is a dictionary

        """ PREFIX CONVENTION:
            const:  numerical values that set the initial conditions (integers normally)
            prob:   numerical values that are used as probabilities (floats from 0 to 1 normally)
            mec:    mechanisms that define the algorithm's behaviour
            data:   descriptors of the algorithm with no impact on its behaviour
        """
        # de qué otra manera podes flexibilizar la convergencia en la UI?

        # general
        cls.instance = instance            # access to current instance of TSP

        # initial population
        cls.const_population_size = 200    # population size: fixed amount of individuals  
        cls.const_city_of_origin = 0       # city of origin: where the salesman starts, changes nothing
        cls.mec_initialization = "random"  # defines how the first generation is produced (at random by default)

        # convergency related
        cls.const_min_generations = 100    # lower bound to avoid early convergency
        cls.const_max_generations = -1     # upper bound to avoid no convergency at all, can be avoided by being set to -1
        cls.const_min_epsilon = 0.001      # convergency related

        # mechanisms that define the next generation
        cls.mec_parent_selection = "default"        # defines how the parents are selected for crossing
        cls.mec_parent_crossover = "default"         # defines how the new individuals are generated from the parents
        cls.mec_individual_mutation = "default"     # defines the mutations applied to some of the new individuals
        cls.mec_individual_survival = "default"     # defines the selection of survivors for the next generation

        # probabilities that define the next generation
        cls.prob_crossing = 0.5
        cls.prob_mutation = 0.5

        # constants that define the next generation
        cls.const_mating_pool_size = cls.const_population_size
        cls.const_offspring_pool_size = cls.const_population_size

        # analytics: description of the execution
        cls.data_best_solution_gen = None  
            # generation:   best solution found for this instance in the current generation of the execution
        cls.data_best_solution_exe = None
            # execution:    best solution found for this instance in all the execution
        cls.data_best_solution_abs = None      
            # absolute:     best solution found for this instance (can be from literature or previous executions)


    def update_parameters(cls, metadata):
        for key, value in metadata.items():
            if hasattr(cls, key):  # Validate that the attribute exists
                setattr(cls, key, value)
            else:
                print(f"Warning: Unknown parameter '{key}'")
        return None

    def run(cls):

        min_gens = cls.const_min_generations
        gen_counter = 0

        # primera generacion
        actual_gen = Generation(mec_initialization=cls.mec_initialization, population_size=cls.const_population_size, instance_size=cls.instance.dimension, origin=cls.const_city_of_origin, instance=cls.instance) # primera generacion
        actual_gen.display()
        print(actual_gen.getBest()[1])
        #print(actual_gen.getBest()[0].display())

        # mejores soluciones: se guarda la solucion, el fitness y la generación a la que pertenece. En el caso de la absoluta se guarda además cómo se obtuvo (literatura o id de ejecución previa)
        best_solution_abs_current = cls.data_best_solution_abs
        best_solution_abs_previous = None
        best_solution_exe_current = None
        best_solution_exe_previous = None
        best_solution_current_gen = actual_gen.getBest()
        best_solution_previous_gen = None

        parent_selection = Selection(cls.mec_parent_selection)
        mating_pool_size = cls.const_mating_pool_size       # por defecto es igual al tamaño de la población
        parent_selection_within_mating_pool = Selection(None,"uniform_selection")
        offspring_pool_size = cls.const_offspring_pool_size
        parent_crossover = Crossover(cls.mec_parent_crossover)
        #offspring_mutation = Mutation()




        while (gen_counter < min_gens): # convergencia

            print("Gen #",gen_counter)
            actual_gen.display()
            print(actual_gen.getBest()[1])
            print()

            individuals = actual_gen.getIndividuals()
            
            # registro de las mejores soluciones hasta el momento
            
            # seleccion de padres: definición del mating pool
            population = actual_gen.getFitnessList()    # lista de los fitness en orden, debe tener el tamaño de la población
            #print("List of fitness:",population)
            mating_pool = parent_selection.run(population,mating_pool_size)
            #print("Mating pool:",mating_pool)

            # cruzamiento
            offspring_pool = []
            while (len(offspring_pool) < offspring_pool_size):
                parents = parent_selection_within_mating_pool.run(list(individuals),2)
                offsprings = parent_crossover.run([individuals[parents[0]],individuals[parents[1]]])
                for offspring in offsprings:
                    if len(offspring_pool) < offspring_pool_size:
                        offspring_pool.append(offspring)
                        #print(offspring)

            # mutaciones

            # seleccion de sobrevivientes
            actual_gen.individuals = []
            for offspring in offspring_pool:
                new_individual = Individual(actual_gen,cls.instance,values=offspring)
                actual_gen.individuals.append(new_individual)

            # obtencion de la nueva generacion y se repite el ciclo
            gen_counter += 1

        print("END")

if __name__=="__main__":
    instance = TSPInstanceParser.parse("../data/br17.atsp")
    ea = EvolutiveAlgorithm(instance,None)
    ea.run()



