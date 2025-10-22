import time

class Convergence:

    default = "min_gen"

    def __init__(self,args):

        self.conjunction = []

        # counters
        self.gen_counter = 0
        self.start_time = time.monotonic()

        # feedback
        self.why_reached = ""

        # dynamic criteria (comes from configuration)
        for key in args:    # creación dinámica de conjunción de condiciones
            if (args[key] != -1):
                #print(f"mec_convergence_{str(key)}, value: {args[key]}")
                self.conjunction.append(getattr(self, f"mec_convergence_{str(key)}", None))
                setattr(self,key,args[key]) # creación dinámica de atributos de instancia
        
        #self.min_gens = args["min_gens"]             # args: [min_gens,max_gens,time_limit,target_fitness,epsilon]
        #self.max_gens = args["max_gens"]  
        #self.target_fitness = args["target_fitness"]

    # BURN-IN: condición mínima

    # no converge a menos que haya llegado al mínimo de generaciones
    def mec_convergence_min_gens(self,ea_args):
        if (self.gen_counter < self.min_gens):
            raise NotYet
        else:
            return False
    
    # DISYUNCIÓN

    # converge una vez que llega a las max_gens generaciones
    def mec_convergence_max_gens(self,ea_args):
        return self.gen_counter >= self.max_gens # 
    
    # converge una vez que se ejecutó durante una cantidad de tiempo determinada en [s]
    def mec_convergence_time_upper_bound(self,ea_args):
        return self.exe_time >= self.time_upper_bound
    
    # converge una vez que se alcanza o supera un fitness específico
    def mec_convergence_target_fitness(self,ea_args):
        return ea_args["best_fitness_in_gen"] <= self.target_fitness
    
    # RELATIVAS A LA DIVERSIDAD: por implementar

    def mec_convergence_epsilon(self,ea_args):
        print(self.epsilon) # variable "de regalo"
        return False
    
    def mec_convergence_stable_population(self,ea_args):
        # el promedio de fitness de la población se mantiene constante
        print(self.stable_population) # variable "de regalo"
        return False

    ####

    # ea passes only what is strictly necessary as arguments
    def reached(self,ea_args):
        self.gen_counter += 1
        self.exe_time = time.monotonic() - self.start_time
        #print(self.exe_time)
        try:
            for condition in self.conjunction:
                #print(condition.__name__)
                if (condition(ea_args)):
                    self.why_reached = f"The EA converged due to {condition.__name__}"  # mejorar el formato más adelante, segun lo que quiera informar
                    print(self.why_reached) 
                    return True
        except NotYet: 
            return False
        return False
    
class NotYet(Exception):
    pass

## TESTING
        
class Converged(Exception):
    pass

if __name__=="__main__":
    x = Convergence({"min_gens": 100, "max_gens": 10000, "time_upper_bound": 10, "target_fitness": 0})
    for _ in range(0,1000000):
        if (x.reached({"best_fitness": 1})):
            raise Converged