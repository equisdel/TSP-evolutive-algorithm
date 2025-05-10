from itertools import accumulate
import random


class ParentSelection:

    default = "FPS"

    def __init__(self,mec_parent_selection):    # receives a function as parameter (?)
        
        self.mec_name = mec_parent_selection
    
        if (mec_parent_selection!=None):      # primera generación
            
            method_name = f"mec_parent_selection_{self.mec_name if mec_parent_selection!='default' else self.default}"
            self.mec = getattr(self, method_name, None)

    # Receives a probability and selects n samples
    def roulette(self,probabilities,sample_size=1):
        accumulated_probabilities = list(accumulate(probabilities))
        #print(accumulated_probabilities)
        #print(r)
        selected = []
        for sample in range(0,sample_size):
            print(sample)
            r = random.uniform(0,1)
            for i,value in enumerate(accumulated_probabilities):
                if r < value:
                    selected.append(i)
                    break
        return selected
    
    def mec_parent_selection_FPS(self,sample_size,population):
        suma = sum(population)
        probabilities = [x/suma for x in population]
        print(probabilities)
        return self.roulette(probabilities,sample_size)

    def run(self,sample_size,population):
        return self.mec(sample_size,population)


if __name__ == "__main__":
    
    # Receives a probability and selects n samples
    def roulette(probabilities,sample_size=1):
        accumulated_probabilities = list(accumulate(probabilities))
        #print(accumulated_probabilities)
        #print(r)
        selected = []
        for sample in range(0,sample_size):
            print(sample)
            r = random.uniform(0,1)
            for i,value in enumerate(accumulated_probabilities):
                if r < value:
                    selected.append(i)
                    break
        return selected
    

    def mec(sample_size,population):
        suma = sum(population)
        probabilities = [x/suma for x in population]
        print(probabilities)
        return roulette(probabilities,sample_size)

    returned = mec(3,population=[50,5,144])
    print(returned)
    #selmec = SelectionMechanism(mec,population={1,2,3})
    #selmec.run(population={1,2,3})