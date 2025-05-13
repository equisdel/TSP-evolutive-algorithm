import random
import time
from TSPInstance import TSPInstanceParser
from EvolutiveAlgorithm import EvolutiveAlgorithm

class TestPlatform:

    def __init__(self,instance,ea):
        self.instance = instance
        self.ea = ea

    def run(self,population_size,min_generations):
        self.ea.run()
        return ea.data_best_solutions_abs[0]

        



if __name__ == "__main__":

    instance = TSPInstanceParser.parse("../data/br17.atsp")
    ea = EvolutiveAlgorithm(instance,None)
    
    seeds = [42, 23, 100, 1, 9, 55, 57, 21, 8, 84]  # 10 tests
    #seeds = [84]
    
    # TEST PARAMETERS
    # 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000
    f1 = 500     # F1: size of population
    f2 = 500     # F2: min number of generations


    ea.const_population_size = f1
    ea.const_min_generations = f2

    tp = TestPlatform(instance,ea)
    best_solutions = []

    start_time = time.perf_counter()  # Record the start time

    for i, seed in enumerate(seeds):
        print(f"Iteration #{i+1}")
        random.seed(seed)
        best_solutions.append(tp.run(f1, f2))

    end_time = time.perf_counter()  # Record the end time
    elapsed_time = end_time - start_time

    print(best_solutions)
    print("Average best:",sum(best_solutions) / len(best_solutions))
    print("Total time (for 10 tests):",elapsed_time)

    # F1:10  , F2:10   ,     : 119, 125, 123, 125, 109, 91 , 148, 134, 72 , 131 :   AvgBest: 117.7 | TotalTime:    0.04
    # F1:10  , F2:50   ,     : 106, 94 , 80 , 101, 85 , 91 , 95 , 109, 72 , 100 :   AvgBest:  93.3 | TotalTime:    0.16
    # F1:10  , F2:100  ,     : 81 , 63 , 80 , 96 , 85 , 91 , 95 , 107, 72 , 100 :   AvgBest:  87.0 | TotalTime:    0.29
    # F1:10  , F2:200  ,     : 81 , 63 , 80 , 96 , 71 , 91 , 78 , 85 , 72 , 76  :   AvgBest:  79.3 | TotalTime:    0.69
    # F1:10  , F2:500  ,     : 70 , 63 , 71 , 61 , 62 , 76 , 78 , 67 , 72 , 70  :   AvgBest:  69.0 | TotalTime:    1.61
    # F1:10  , F2:1000 ,     : 70 , 61 , 71 , 61 , 62 , 69 , 53 , 67 , 64 , 54  :   AvgBest:  63.2 | TotalTime:    2.89
    # F1:10  , F2:2000 ,     : 54 , 61 , 57 , 61 , 62 , 65 , 53 , 60 , 64 , 54  :   AvgBest:  59.1 | TotalTime:    5.98
    # F1:10  , F2:5000 ,     : 54 , 61 , 52 , 61 , 61 , 60 , 53 , 60 , 56 , 54  :   AvgBest:  57.2 | TotalTime:   12.41
    # F1:10  , F2:10000,     : 54 , 54 , 52 , 55 , 61 , 60 , 53 , 60 , 56 , 54  :   AvgBest:  55.9 | TotalTime:   26.61

    # F1:50  , F2:10   ,     : 77 , 93 , 61 , 93 , 102, 118, 98 , 88 , 81 , 89  :   AvgBest:  90.0 | TotalTime:    0.16
    # F1:50  , F2:50   ,     : 77 , 72 , 56 , 70 , 85 , 66 , 85 , 88 , 48 , 76  :   AvgBest:  72.3 | TotalTime:    0.65
    # F1:50  , F2:100  ,     : 75 , 60 , 56 , 70 , 73 , 66 , 85 , 74 , 48 , 76  :   AvgBest:  68.3 | TotalTime:    1.35
    # F1:50  , F2:200  ,     : 54 , 60 , 56 , 70 , 52 , 66 , 63 , 69 , 48 , 74  :   AvgBest:  61.2 | TotalTime:    2.59
    # F1:50  , F2:500  ,     : 54 , 60 , 56 , 60 , 52 , 63 , 59 , 59 , 48 , 69  :   AvgBest:  58.0 | TotalTime:    6.53
    # F1:50  , F2:1000 ,     : 54 , 60 , 45 , 60 , 52 , 57 , 59 , 59 , 48 , 63  :   AvgBest:  55.7 | TotalTime:   13.30
    # F1:50  , F2:2000 ,     : 54 , 60 , 45 , 60 , 52 , 50 , 53 , 45 , 48 , 60  :   AvgBest:  52.7 | TotalTime:   24.54
    # F1:50  , F2:5000 ,     : 54 , 56 , 45 , 44 , 51 , 50 , 53 , 45 , 48 , 52  :   AvgBest:  49.8 | TotalTime:   63.28
    # F1:50  , F2:10000,     : 42 , 49 , 45 , 44 , 51 , 47 , 53 , 45 , 48 , 52  :   AvgBest:  47.6 | TotalTime:  121.39

    # F1:100 , F2:10   ,     : 76 , 113, 76 , 81 , 89 , 69 , 77 , 88 , 63 , 85  :   AvgBest:  81.7 | TotalTime:    0.32
    # F1:100 , F2:50   ,     : 66 , 78 , 74 , 70 , 70 , 64 , 77 , 82 , 63 , 69  :   AvgBest:  71.3 | TotalTime:    1.73
    # F1:100 , F2:100  ,     : 66 , 64 , 74 , 70 , 65 , 64 , 63 , 64 , 63 , 69  :   AvgBest:  66.2 | TotalTime:    3.13
    # F1:100 , F2:200  ,     : 49 , 64 , 57 , 68 , 47 , 49 , 63 , 61 , 63 , 62  :   AvgBest:  58.3 | TotalTime:    5.74
    # F1:100 , F2:500  ,     : 49 , 52 , 57 , 61 , 47 , 49 , 60 , 61 , 53 , 62  :   AvgBest:  55.1 | TotalTime:   14.43
    # F1:100 , F2:1000 ,     : 49 , 52 , 52 , 61 , 47 , 49 , 60 , 61 , 51 , 58  :   AvgBest:  54.0 | TotalTime:   38.55
    # F1:100 , F2:2000 ,     : 47 , 47 , 52 , 60 , 47 , 49 , 49 , 61 , 51 , 55  :   AvgBest:  51.8 | TotalTime:   53.44
    # F1:100 , F2:5000 ,     : 47 , 47 , 52 , 52 , 47 , 49 , 49 , 50 , 51 , 55  :   AvgBest:  49.9 | TotalTime:  136.66
    # F1:100 , F2:10000,     : 45 , 47 , 47 , 50 , 44 , 49 , 47 , 50 , 51 , 50  :   AvgBest:  48.0 | TotalTime:  277.56

    # F1:200 , F2:10   ,     : 75 , 77 , 72 , 85 , 76 , 76 , 59 , 66 , 63 , 89  :   AvgBest:  73.8 | TotalTime:    1.60
    # F1:200 , F2:50   ,     : 70 , 67 , 68 , 56 , 62 , 61 , 59 , 66 , 63 , 76  :   AvgBest:  64.8 | TotalTime:    3.38
    # F1:200 , F2:100  ,     : 61 , 61 , 62 , 56 , 62 , 54 , 52 , 62 , 60 , 58  :   AvgBest:  58.8 | TotalTime:    6.95
    # F1:200 , F2:200  ,     : 58 , 61 , 56 , 51 , 62 , 54 , 52 , 57 , 60 , 58  :   AvgBest:  56.9 | TotalTime:   13.69
    # F1:200 , F2:500  ,     : 58 , 54 , 52 , 51 , 58 , 54 , 52 , 57 , 57 , 58  :   AvgBest:  55.1 | TotalTime:   31.96
    # F1:200 , F2:1000 ,     : 48 , 54 , 52 , 51 , 54 , 54 , 52 , 57 , 47 , 50  :   AvgBest:  51.9 | TotalTime:   63.19
    # ___
    # ___
    # ___

    # F1:500 , F2:10   ,     : 50 , 70 , 80 , 73 , 62 , 62 , 49 , 70 , 69 , 65  :   AvgBest:  65.0 | TotalTime:    4.67
    # F1:500 , F2:50   ,     : 50 , 68 , 60 , 61 , 62 , 52 , 49 , 57 , 55 , 60  :   AvgBest:  57.4 | TotalTime:   20.84
    # F1:500 , F2:100  ,     : 50 , 49 , 60 , 48 , 62 , 52 , 49 , 57 , 55 , 60  :   AvgBest:  54.2 | TotalTime:   42.98
    # F1:500 , F2:200  ,     : 50 , 49 , 60 , 48 , 57 , 52 , 49 , 57 , 50 , 60  :   AvgBest:  53.2 | TotalTime:   86.87
    # F1:500 , F2:500  ,     : 48 , 49 , 52 , 47 , 49 , 52 , 49 , 49 , 50 , 57  :   AvgBest:  50.2 | TotalTime:  221.93
    # F1:500 , F2:1000 ,     : 48 , 49 , 47 , 47 , 47 , 52 , 49 , 49 , 50 , 51  :   AvgBest:  48.9 | TotalTime:  367.51
    # ___
    # ###
    # ###
    
    # F1:1000, F2:10   ,     : 59 , 66 , 73 , 61 , 60 , 69 , 84 , 71 , 63 , 65  :   AvgBest:  67.1 | TotalTime:    8.04
    # F1:1000, F2:50   ,     : 58 , 60 , 53 , 57 , 55 , 58 , 57 , 55 , 63 , 58  :   AvgBest:  57.4 | TotalTime:   36.72
    # F1:1000, F2:100  ,     : 56 , 57 , 53 , 55 , 55 , 55 , 56 , 52 , 55 , 52  :   AvgBest:  54.6 | TotalTime:   78.36
    # F1:1000, F2:200  ,     : 49 , 57 , 52 , 55 , 53 , 55 , 55 , 52 , 55 , 50  :   AvgBest:  53.3 | TotalTime:  154.75
    # F1:1000, F2:500  ,     : 49 , 57 , 52 , 55 , 53 , 55 , 55 , 52 , 55 , 50  :   AvgBest:  50.3 | TotalTime:  385.20
    # F1:1000, F2:1000 ,     : 45 , 50 , 52 , 55 , 52 , 50 , 50 , 47 , 50 , 50  :   AvgBest:  48.7 | TotalTime:  796.75
    # F1:1000, F2:2000 ,     : 45 , 45 , 47 , 48 , 46 , 50 , 46 , 47 , 49 , 47  :   AvgBest:  47.0 | TotalTime: 1519.37
    # ###
    # ###

    # F1:2000, F2:10   ,     : 54 , 66 , 54 , 71 , 58 , 65 , 55 , 68 , 62 , 66  :   AvgBest:  61.9 | TotalTime:   46.75
    # F1:2000, F2:50   ,
    # F1:2000, F2:100  ,
    # F1:2000, F2:200  ,
    # ###
    # ###
    # ###
    # ###
    # ###

    # F1:5000, F2:10   ,     : 56 , 54 , 58 , 58 , 56 , 64 , 55 , 64 , 57 , 62  :   AvgBest:  58.4 | TotalTime:  245.11
    # F1:5000, F2:50   ,     : 52 , 50 , 53 , 44 , 55 , 40 , 55 , 51 , 47 , 55  :   AvgBest:  50.2 | TotalTime: 1187.48
    # ###
    # ###
    # ###
    # ### 
    # ###
    # ###
    # ###

    # F1:10000, F2:10   ,     : 55 , 57 , 52 , 58 , 54 , 53 , 55 , 57 , 57 , 61  :   AvgBest:  55.9 | TotalTime: 1452.01
    # ###
    # ###
    # ###
    # ###
    # ###
    # ###
    # ###
    # ###



    

    


    
    
    

    #g = Graph(instance,ea)
    #g.display("best_solutions_graph")

