# it gathers all the parameters from configuration and it runs the simulation
from components.Population import Generation, Individual
from components.MecSelection import Selection
from components.MecCrossover import Crossover
from components.MecMutation import Mutation
# for test
from TSPInstance import TSPInstanceParser

class EvolutiveAlgorithm:

    # when we change from page 3 (parameters) to page 4 (execution) we create this Evolutive Algorithm

    log_path = "..\stats\log_md"

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
        cls.const_population_size = 50     # population size: fixed amount of individuals  
        cls.const_city_of_origin = 0       # city of origin: where the salesman starts, changes nothing
        cls.mec_initialization = "random"  # defines how the first generation is produced (at random by default)

        # convergency related
        cls.const_min_generations = 100    # lower bound to avoid early convergency
        cls.const_max_generations = -1     # upper bound to avoid no convergency at all, can be avoided by being set to -1
        cls.const_min_epsilon = 0.001      # convergency related

        # mechanisms that define the next generation
        cls.mec_parent_selection = "TS"        # defines how the parents are selected for crossing
        cls.mec_parent_crossover = "default"         # defines how the new individuals are generated from the parents
        cls.mec_individual_mutation = "flip"     # defines the mutations applied to some of the new individuals
        cls.mec_individual_survival = "default"     # defines the selection of survivors for the next generation
        cls.mec_offspring_selection = "uniform_selection"

        # probabilities that define the next generation
        cls.prob_crossing = 0.5
        cls.prob_mutation = 1/(instance.get_dimension())

        # constants that define the next generation
        cls.const_mating_pool_size = cls.const_population_size
        cls.const_offspring_pool_size = cls.const_population_size

        # analytics: description of the execution
        cls.data_best_solutions_gen = []  
            # generation:   best solution found for this instance in the current generation of the execution
        cls.data_best_solutions_exe = []
            # execution:    best solution found for this instance in all the execution
        cls.data_best_solutions_abs = []      
            # absolute:     best solution found for this instance (can be from literature or previous executions)

    def writeLog():
        # llamar al terminar
        return

    def update_parameters(cls, metadata):
        for key, value in metadata.items():
            if hasattr(cls, key):  # Validate that the attribute exists
                setattr(cls, key, value)
            else:
                print(f"Warning: Unknown parameter '{key}'")
        return None

    def get_best_solutions(self, generation, best_solution_exe, best_solution_abs):
        best_solution_gen = generation.getBest()[0].getCost()     
        if (best_solution_exe is None or best_solution_gen < best_solution_exe):
            best_solution_exe = best_solution_gen
        if (best_solution_abs is None or best_solution_exe < best_solution_abs):
            best_solution_abs = best_solution_exe
        return best_solution_gen, best_solution_exe, best_solution_abs      # returns best fitness from each scope

    def run(cls):

        try:

            min_gens = cls.const_min_generations
            gen_counter = 0

            # primera generacion
            actual_gen = Generation(mec_initialization=cls.mec_initialization, population_size=cls.const_population_size, instance_size=cls.instance.dimension, origin=cls.const_city_of_origin, instance=cls.instance) # primera generacion
            #actual_gen.display()
            #print(actual_gen.getBest()[1])
            #print(actual_gen.getBest()[0].display())

            # mejores soluciones: se guarda la solucion, el fitness y la generación a la que pertenece. En el caso de la absoluta se guarda además cómo se obtuvo (literatura o id de ejecución previa)
            best_solution_exe = None
            best_solution_abs = None #cls.data_best_solution_abs  # could be None
            best_solutions_gen = [] # starts at index 0 for generation 0
            best_solutions_exe = [] # starts at index 0 for generation 0
            best_solutions_abs = [] # starts at index 0 for generation 0

            parent_selection = Selection(cls.mec_parent_selection)
            mating_pool_size = cls.const_population_size       # por defecto es igual al tamaño de la población
            parent_selection_within_mating_pool = Selection(None,"uniform_selection")
            parent_crossover = Crossover(cls.mec_parent_crossover)
            offspring_pool_size = cls.const_population_size
            #print("offspring_pool_size:",offspring_pool_size)
            offspring_selection = Selection(None,internal_selection="uniform_selection")
            offspring_mutation = Mutation(cls.mec_individual_mutation)

            while (gen_counter < min_gens): # convergencia

                #print(actual_gen.getBest()[1])
                #print()
                #print(gen_counter)
                #print("   Gen #",gen_counter)
                actual_gen.display()
                #print("!!:",len(actual_gen.individuals))

                individuals = actual_gen.getIndividuals()
                
                # registro de las mejores soluciones hasta el momento
                b_gen, b_exe, b_abs = cls.get_best_solutions(actual_gen,best_solution_exe,best_solution_abs)
                best_solutions_gen.append(b_gen) # starts at index 0 for generation 0
                best_solutions_exe.append(b_exe) # starts at index 0 for generation 0
                best_solutions_abs.append(b_abs) # starts at index 0 for generation 0
                best_solution_exe = b_exe
                best_solution_abs = b_abs
                
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
                #print(offspring_pool)

                # mutaciones
                """
                """
                selected_offsprings_index = offspring_selection.run(population=offspring_pool,sample_size=int(cls.const_population_size/2)) # indexes
                for i in selected_offsprings_index:
                    offspring_pool[i] = offspring_mutation.run(offspring_pool[i])
                        

                # seleccion de sobrevivientes
                actual_gen.individuals = []
                for offspring in offspring_pool:
                    new_individual = Individual(actual_gen,cls.instance,values=offspring)
                    actual_gen.individuals.append(new_individual)

                # obtencion de la nueva generacion y se repite el ciclo
                gen_counter += 1

            cls.data_best_solutions_gen = best_solutions_gen
            cls.data_best_solutions_exe = best_solutions_exe
            cls.data_best_solutions_abs = [best_solution_abs for x in range (0,cls.const_min_generations)]

        except Exception as e:
            raise ValueError("An error occured during the execution of the Evolutive Algorithm:",e)
        
        finally:
            # tiene q escribir si o si en el log
            print(cls.data_best_solutions_exe)
            return



if __name__=="__main__":
    instance = TSPInstanceParser.parse("./data/br17.atsp")
    ea = EvolutiveAlgorithm(instance,None)
    ea.run()
    print(ea.data_best_solutions_abs)



