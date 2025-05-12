from itertools import accumulate
import random


class Selection:

    default = "FPS"

    def __init__(self,mec_parent_selection,internal_selection="stochastic_universal_sampling_selection"):    # receives a function as parameter (?)
        
        self.mec_name = mec_parent_selection
        if (mec_parent_selection!=None):      # primera generación
            
            method_name = f"mec_parent_selection_{self.mec_name if mec_parent_selection!='default' else self.default}"
            self.mec = getattr(self, method_name, None)
            self.internal_mec = internal_selection

        else:
            self.mec = getattr(self,internal_selection,None)



    # Internal selection

    # Receives a probability and selects n samples
    def roulette_wheel_selection(self,probabilities,sample_size=1):
        accumulated_probabilities = list(accumulate(probabilities))
        #print(accumulated_probabilities)
        selected = []
        for sample in range(0,sample_size):
            r = random.uniform(0,1)
            for i,value in enumerate(accumulated_probabilities):
                if r < value:
                    selected.append(i)
                    break
        return sorted(selected)
    
    def stochastic_universal_sampling_selection(self,probabilities,sample_size=1):
        accumulated_probabilities = list(accumulate(probabilities))
        #print(accumulated_probabilities)
        selected = []
        r = random.uniform(0,1/sample_size)
        for sample in range(0,sample_size):
            for i,value in enumerate(accumulated_probabilities):
                if r <= value:
                    selected.append(i)
                    r = r+1/sample_size
                    break
        return selected
    
    def uniform_selection(self, probabilities, sample_size=1):
        selected = random.choices(range(len(probabilities)), k=sample_size)
        #print(selected)
        return selected
    
    def mec_parent_selection_FPS(self,population,sample_size):
        suma = sum(population)
        probabilities = [x/suma for x in population]
        #print(probabilities)
        #print(self.roulette_wheel_selection(probabilities,sample_size))
        return self.stochastic_universal_sampling_selection(probabilities,sample_size)

    def run(self,population,sample_size):
        return self.mec(population,sample_size)


if __name__ == "__main__":
    print("Parent Selection")