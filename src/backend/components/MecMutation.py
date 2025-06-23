import random

class Mutation:

    default = "default"
    # esta parte es general a todos los mecanismos, se puede abstraer como Mechanism con el resto de las clases como hijas
    def __init__(self,mec_mutation,mutation_rate=0.20):

        self.mec_name = mec_mutation
        self.mutation_rate = mutation_rate
        if (mec_mutation!=None):      # primera generación
            method_name = f"mec_mutation_{self.mec_name if mec_mutation!='default' else self.default}"
            self.mec = getattr(self, method_name, None)

    
    # change name later
    def mec_mutation_default(self, individual):
        
        instance_size = len(individual)     # picks as many random values as cities in the instance
        modified_individual = individual
    
        r = [random.uniform(0,1) for _ in range(instance_size)]

        # select bits to modify
        bits_to_modify = []
        for i in range(instance_size):    
            if (r[i] < self.mutation_rate):
                bits_to_modify = bits_to_modify + [i]
        random.shuffle(bits_to_modify)
       
        # exchange them randomly in pairs
        for i in range(0,len(bits_to_modify)-len(bits_to_modify)%2,2):
            modified_individual[bits_to_modify[i]], modified_individual[bits_to_modify[i+1]] = modified_individual[bits_to_modify[i+1]], modified_individual[bits_to_modify[i]]
    
        return modified_individual

    def mec_mutation_flip(self, individual):
        
        instance_size = len(individual)     # picks as many random values as cities in the instance
        modified_individual = individual

        r = [random.uniform(0,1) for _ in range(instance_size)]
        direction = random.choice([True, False])         # mutation can be left to right or right to left
    
        for i in range(instance_size):      # for each bit, if random is within threshold, flips bit with its neighbour
            if r[i] < self.mutation_rate:
                if direction and i < instance_size-1:
                    modified_individual[i], modified_individual[i+1] = individual[i+1], individual[i]
                elif not direction and i > 0:
                    modified_individual[i], modified_individual[i-1] = individual[i-1], individual[i]
        return modified_individual

    # abstract method, change later
    def run(self,individual):
        origin = individual[0]
        ind = individual.copy()[1:-1]   # removes origin for faster processing
        return [origin] + self.mec(ind) + [origin]

if __name__ == "__main__":
    mm = Mutation("flip", mutation_rate=0.25)
    print(mm.run([0,1,2,3,4,5,6,7,8,9,0]))
