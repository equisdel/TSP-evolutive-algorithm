import random

class Crossover:

    # Mechanisms from theory: OPC, PMX, 

    default = "OPC" # One-Point-Crossover

    def __init__(self,mec_parent_crossover):

        self.mec_name = mec_parent_crossover
        if (mec_parent_crossover!=None):      # primera generación
            
            method_name = f"mec_parent_crossover_{self.mec_name if mec_parent_crossover!='default' else self.default}"
            self.mec = getattr(self, method_name, None)
    

    def mec_parent_crossover_OPC(self,parents):

        min_parents,    max_parents     = 2,2
        min_offsprings, max_offsprings  = 2,2

        if (len(parents) not in range(min_parents,max_parents+1)):
            print("The crossover mechanism chosen is not available for",len(parents),"parents!")
        else:
            offspring1, offspring2 = [], []
            parent1, parent2 = parents[0].getValues(), parents[1].getValues()    # individual
            values_size = len(parent1)
            r = random.randint(1,values_size-1)
            # first section
            #print(parent1,parent2)
            for i in range(0,r):
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
                #print(offspring1,offspring2)
            # second section
            left_parent1, left_parent2 = [x for x in parent1 if x not in offspring2], [x for x in parent2 if x not in offspring1]
            #print(r,left_parent1,values_size-r+1)
            #print(r,left_parent2,values_size-r+1)
            for i in range(0,values_size-r-1):
                offspring1.append(left_parent2[i])
                offspring2.append(left_parent1[i])
            offspring1.append(offspring1[0])
            offspring2.append(offspring2[0])
            return [offspring1, offspring2]
        return None

    def mec_parent_crossover_PMX(self,parents):

        parent1, parent2 = parents[0].getValues(), parents[1].getValues()
        #parent1, parent2 = parents[0], parents[1]
        offspring1, offspring2 = [], []

        instance_size = len(parent1)

        bit_map = [random.choice([0,1]) for _ in range(instance_size)]

        for i,value in enumerate(bit_map):
            if value==0:
                if (parent1[i] not in offspring1): 
                    offspring1.append(parent1[i])
                if (parent2[i] not in offspring2): 
                    offspring2.append(parent2[i])
            elif value==1:
                if (parent2[i] not in offspring1): 
                    offspring1.append(parent2[i])
                if (parent1[i] not in offspring2): 
                    offspring2.append(parent1[i])

        return [offspring1, offspring2]
    
    def run(self,parents):
        return self.mec(parents)
    
if __name__ == "__main__":
    x = Crossover("PMX")
    p1 = [10,2,30,4,50,6,70]
    p2 = [1,20,3,40,5,60,7]
    p = [p1,p2]
    print(x.mec_parent_crossover_PMX(p))
