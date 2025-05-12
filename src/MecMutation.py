import random

class Mutation:

    default = "default"
    # esta parte es general a todos los mecanismos, se puede abstraer como Mechanism con el resto de las clases como hijas
    def __init__(self,mec_mutation):

        self.mec_name = mec_mutation
        if (mec_mutation!=None):      # primera generación
            method_name = f"mec_mutation_{self.mec_name if mec_mutation!='default' else self.default}"
            self.mec = getattr(self, method_name, None)

    
    # change name later
    def mec_mutation_default(self, individual):
        i, j = random.sample(range(len(individual)), 2) # picks two different random values
        modified_individual = individual
        modified_individual[i], modified_individual[j] = individual[j], individual[i]
        return modified_individual

    # abstract method, change later
    def run(self,individual):
        origin = individual[0]
        ind = individual.copy()[1:-1]
        return [origin] + self.mec(ind) + [origin]

if __name__ == "__main__":
    mm = Mutation("default")
    print(mm.run([0,1,2,3,4,5,6,7,8,9,0]))
