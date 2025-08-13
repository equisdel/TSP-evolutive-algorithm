from itertools import accumulate
import random
import math

class Selection:

    default = "FPS"     # Fitness Proportional Selection

    def __init__(self,mec_parent_selection,internal_selection="stochastic_universal_sampling_selection"):    # receives a function as parameter (?)
        
        self.mec_name = mec_parent_selection
        if (mec_parent_selection!=None):      # primera generación
            
            method_name = f"mec_parent_selection_{self.mec_name if mec_parent_selection!='default' else self.default}"
            self.mec = getattr(self, method_name, None)
            self.internal_mec = getattr(self, internal_selection)

        else:
            self.mec = getattr(self,internal_selection,None)


    # Internal selection: returns #sample_size indexes (with repetition)

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
    
    # Slightly better than roulette wheel selection, it is more uniform and less prone to selection pressure
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
    
    # Uniform selection, picks n random samples from the population
    def uniform_selection(self, probabilities, sample_size=1):
        selected = random.choices(range(len(probabilities)), k=sample_size)
        #print(selected)
        return selected

    # Parent Selection: population is a list of fitness values

    # FPS: Fitness Proportional Selection
    def mec_parent_selection_FPS(self,population,sample_size):
        suma = sum(population)
        probabilities = [x/suma for x in population]
        #print(probabilities)
        #print(self.roulette_wheel_selection(probabilities,sample_size))
        return self.internal_mec(probabilities,sample_size)

    # RBS: Rank-Based Selection (linear mapping)
    def mec_parent_selection_RBS(self,population,sample_size,s=1):
        if s < 1 or s > 2:
            raise ValueError("Rank-Based Selection: The parameter 's' must be in the range [1, 2].")
        else:
            population_size = len(population)
            ranking = sorted(range(population_size), key=lambda i: population[i], reverse=True)
            probabilities = [((2-s)/population_size + 2*i*(s-1)/(population_size*(population_size-1))) for i in ranking]
            #print(probabilities)
            return self.internal_mec(probabilities,sample_size)

    # TS: Tournament Selection
    def mec_parent_selection_TS(self,population,sample_size,p=1.0,k=3):
        if (k > len(population)):
            raise ValueError("Tournament Selection: The parameter 'k' must be in the range [1,population_size]")
        if (p <= 0 or  p > 1):
            raise ValueError("Tournament Selection: The parameter 'p' must be in the range (0,1]")
        else:
            selected = []
            for _ in range(sample_size):
                tournament_participants = self.uniform_selection(population,sample_size=k)                          # i have k participants (or their indexes in the population)
                sorted_participants = sorted(tournament_participants, key=lambda i: population[i], reverse=True)    # now i have them sorted by fitness from highest to lowest
                probabilities = [p*((1-p)**i) for i in range(k)]                                                    # p will determine how likely it is to pick the best (selective pressure)
                selected = selected + [sorted_participants[self.stochastic_universal_sampling_selection(probabilities,1)[0]]]   # the chosen one is added to the selection
            return selected

    # RUN
    def run(self,population,sample_size):
        if (sample_size > len(population)):
            raise ValueError("Parent Selection: The size of the mating pool can't be bigger than the population size.")
        else:
            return self.mec(population,sample_size)


if __name__ == "__main__":
    print("Parent Selection")
    x = Selection(mec_parent_selection="mec_parent_selection_TS")
    print(x.mec_parent_selection_TS([1000,2000,3000,4000,5000,6000,7000,8000,9000,100000],3,k=3))