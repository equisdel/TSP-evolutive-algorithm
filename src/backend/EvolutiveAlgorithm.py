# it gathers all the parameters from configuration and it runs the simulation
from backend.components.Population import Generation, Individual
from backend.components.MecSelection import Selection
from backend.components.MecSurvivorSelection import SurvivorSelection
from backend.components.MecCrossover import Crossover
from backend.components.MecMutation import Mutation
from backend.components.MecConvergence import Convergence
# for test
from backend.TSPInstance import TSPInstanceParser
from PySide6.QtCore import QObject, Signal
import random

class EvolutiveAlgorithm(QObject):

    # when we change from page 3 (parameters) to page 4 (execution) we create this Evolutive Algorithm
    
    data_updated = Signal(list, list, list)     # actualización del gráfico

    def __init__(cls,instance,config):    
        super().__init__()        
        cls.config = config.get_json_config()  # has its id
        cls.instance = instance     # has its id, access to current instance of TSP

    def update_config(cls,new_config):
        cls.config = new_config

    def load_parameters(cls):       # first thing it will call when execution starts

        """ PREFIX CONVENTION:
            const:  numerical values that set the initial conditions (integers normally)
            prob:   numerical values that are used as probabilities (floats from 0 to 1 normally)
            mec:    mechanisms that define the algorithm's behaviour
            data:   descriptors of the algorithm with no impact on its behaviour
        """

        # initial population
        cls.const_population_size = cls.config["initialization"]["population size"].get_value()     # population size: fixed amount of individuals  
        cls.const_city_of_origin = cls.config["initialization"]["city of origin"].get_value()        # city of origin: where the salesman starts, changes nothing
        cls.mec_initialization = cls.config["initialization"]["mechanism"].get_value()   # defines how the first generation is produced (at random by default)

        # convergency related
        cls.const_min_generations = cls.config["termination criteria"]["min generations"].get_value()    # lower bound to avoid early convergency
        cls.const_max_generations = cls.config["termination criteria"]["max generations"].get_value()     # upper bound to avoid no convergency at all, can be avoided by being set to -1
        cls.const_min_epsilon = cls.config["termination criteria"]["epsilon"].get_value()     # convergency related

        # mechanisms that define the next generation
        cls.mec_parent_selection = cls.config["parent selection"]["mechanism"].get_value()        # defines how the parents are selected for crossing
        cls.mec_parent_crossover = cls.config["crossover"]["mechanism"].get_value()        # defines how the new individuals are generated from the parents
        cls.mec_individual_mutation = cls.config["offspring mutation"]["mechanism"].get_value()     # defines the mutations applied to some of the new individuals
        cls.mec_survivor_selection = cls.config["survivor selection"]["mechanism"].get_value()    # defines the selection of survivors for the next generation
        # cls.mec_offspring_selection = "uniform_selection"
        # probabilities that define the next generation
        cls.prob_crossing = cls.config["crossover"]["probability"].get_value()
        cls.prob_mutation = cls.config["offspring mutation"]["probability"].get_value()  #1/(instance.get_dimension())
        print("ok") 

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

    # EXECUTION

    def run(cls,ea):

        try:

            cls.load_parameters()       # loads the parameters
            print("no errors after loading parameters")
            min_gens = cls.const_min_generations
            #gen_counter = 0

            # primera generacion
            actual_gen = Generation(mec_initialization=cls.mec_initialization, population_size=cls.const_population_size, instance_size=cls.instance.dimension, origin=cls.const_city_of_origin, instance=cls.instance) # primera generacion
            #actual_gen.display()
            #print(actual_gen.getBest()[1])
            #print(actual_gen.getBest()[0].display())

            # mejores soluciones: se guarda la solucion, el fitness y la generación a la que pertenece. En el caso de la absoluta se guarda además cómo se obtuvo (literatura o id de ejecución previa)
            best_solution_exe = None
            best_solution_abs = cls.instance.get_absolute_best()    # could be None
            best_solutions_gen = [] # starts at index 0 for generation 0
            best_solutions_exe = [] # starts at index 0 for generation 0
            best_solutions_abs = [] # starts at index 0 for generation 0

            # seteo de configuracion del algoritmo
            population_size = cls.const_population_size
            parent_selection = Selection(cls.mec_parent_selection)
            mating_pool_size = population_size        # por defecto es igual al tamaño de la población
            #parent_selection_within_mating_pool = Selection(None,"uniform_selection")  # error conceptual, no existe
            parent_crossover = Crossover(cls.mec_parent_crossover)
            offspring_pool_size = population_size     # por defecto es igual al tamaño de la población
            offspring_mutation = Mutation(cls.mec_individual_mutation)
            offspring_selection = Selection(None,internal_selection="uniform_selection")
            survivor_selection = SurvivorSelection(cls.mec_survivor_selection)
            convergence = Convergence({"min_gens": 10, "max_gens": cls.const_min_generations})

            while (not convergence.reached(None)):
            #while (gen_counter < min_gens): # convergencia

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
                mating_pool = parent_selection.run(population,mating_pool_size) # el tamaño del mating pool es igual al tamaño poblacional
                print("Mating pool:",mating_pool)

                # cruzamiento
                offspring_pool = []
                random.shuffle(mating_pool)
                parents1_indexes, parents2_indexes = mating_pool[0:int(population_size/2)], mating_pool[int(population_size/2):]
                for i in range(0,int(population_size/2)):
                    #print("indexes of adam and eve:",parents1_indexes[i],parents2_indexes[i])
                    #print("adam and eve themselves:",[individuals[parents1_indexes[i]]],[individuals[parents2_indexes[i]]])
                    #print("their fitnesses:",individuals[parents1_indexes[i]].getFitness(),individuals[parents2_indexes[i]].getFitness())
                    #print("their values:",individuals[parents1_indexes[i]].getValues(),individuals[parents2_indexes[i]].getValues())
                    offsprings = parent_crossover.run([individuals[parents1_indexes[i]],individuals[parents2_indexes[i]]])
                    for offspring in offsprings:
                        offspring_pool.append(offspring)
                print(len(offspring_pool) == population_size)

                # mutaciones sobre nuevos individuos
                selected_offsprings_index = offspring_selection.run(population=offspring_pool,sample_size=int(cls.const_population_size/2)) # indexes
                for i in selected_offsprings_index:
                    offspring_pool[i] = offspring_mutation.run(offspring_pool[i])
                
                # seleccion de sobrevivientes: esto está mal
                """
                actual_gen.individuals = []
                """
                new_individuals = []
                for offspring in offspring_pool:
                    new_individual = Individual(actual_gen,cls.instance,values=offspring)
                    new_individuals.append(new_individual)

                # esto es reemplazo generacional
                actual_gen.individuals = survivor_selection.run(actual_gen.individuals,new_individuals)

                # obtencion de la nueva generacion y se repite el ciclo
                ea.data_updated.emit(best_solutions_gen, best_solutions_exe, [best_solution_abs for _ in range (0,len(best_solutions_gen))])
                #gen_counter += 1

            print(f"convergio por {convergence.why_reached}")
            cls.data_best_solutions_gen = best_solutions_gen
            cls.data_best_solutions_exe = best_solutions_exe
            cls.data_best_solutions_abs = [best_solution_abs for _ in range (0,len(cls.data_best_solutions_gen))]

        except Exception as e:
            print(e)
            raise ValueError("An error occured during the execution of the Evolutive Algorithm:",e)
        
        finally:
            # tiene q escribir si o si en el log
            #print(cls.data_best_solutions_exe)
            return


    def write_log(self):
        # escritura en la base de datos: configuracion y ejecucion
        return

    def get_best_solutions(self, generation, best_solution_exe, best_solution_abs):
        best_solution_gen = generation.getBest()[0].getCost()     
        print("!",best_solution_gen)
        if (best_solution_exe is None or best_solution_gen < best_solution_exe):
            best_solution_exe = best_solution_gen
        if (best_solution_abs is None or best_solution_exe < best_solution_abs):
            best_solution_abs = best_solution_exe
        return best_solution_gen, best_solution_exe, best_solution_abs      # returns best fitness from each scope

    @classmethod
    def get_default_configuration(cls):
        global default_config
        return default_config
    


if __name__=="__main__":
    instance = TSPInstanceParser.parse("./data/instances/ba6.atsp")
    ea = EvolutiveAlgorithm(instance)
    #ea.run()
    print(ea.config["initial population"]["size"])
    #print(ea.data_best_solutions_abs)



