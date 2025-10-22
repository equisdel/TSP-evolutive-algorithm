class SurvivorSelection():

    default = "generational"

    def __init__(self,mec_name):
        print()
        #self.model = default_model
        self.mec_name = mec_name
        method_name = f"mec_survivor_selection_{self.mec_name if mec_name!='default' else self.default}"
        self.mec = getattr(self, method_name, None)
        print("mec created")

    # modelo generacional: (μ,λ)
    def mec_survivor_selection_generational(self,old_individuals,new_individuals):
        next_gen = []
        if (len(old_individuals) <= len(new_individuals)):
            if (len(old_individuals) == len(new_individuals)):  # no hay exceso de offsprings: λ=μ 
                next_gen = new_individuals
            else:                                               # hay exceso de offsprings:    λ>μ  
                print("no esta implementado aun, debería usar un mecanismo de selección interna")
        else:   # no es válido para este modelo 
            print("Generational Survivor Selection: Not enough offsprings to apply (must be >= ",len(old_individuals),").")
        return next_gen

    # modelo steady_state
    #def mec_survivor_selection_steady_state(self,old_individuals,new_individuals,n=1/len(old_individuals),termination_selection,offspring_selection=None):
    #    next_gen = []
        # Iterate old individuals
        # Ruletealos con el mecanismo interno de seleccion o con otra cosa (depende del criterio)
        # Si toca reemplazo selecciono del pool de offsprings (depende del criterio)
        # Reemplazo al actual
    #    return next_gen

    def run(self,actual_gen,offspring_pool): # ambas son listas de individuos
        next_gen = self.mec(actual_gen,offspring_pool)
        return next_gen # next_gen es una selección de individuos

if __name__=="__main__":
    print("Survivor selection")