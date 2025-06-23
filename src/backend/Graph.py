import matplotlib
import random
from TSPInstance import TSPInstanceParser
from EvolutiveAlgorithm import *

matplotlib.use('TkAgg')  # or 'Agg' if no GUI is needed

import matplotlib.pyplot as plt


# singleton
class Graph:
    
    def __init__(self,instance,evolutive_algorithm):
        self.instance = instance
        self.evolutive_algorithm = evolutive_algorithm

    def display(self,graph_name):
        method_name = f"calculate_{graph_name}"
        method = getattr(self, method_name, None)
        if method:
            data_series = method()
            for series in data_series:
                plt.plot(
                    series["x"], 
                    series["y"], 
                    series.get("style", "-"),
                    label=series.get("label", "")
                )
            plt.legend()
            plt.title(graph_name.replace("_", " ").title())
            plt.grid(True)
            plt.show()

    def calculate_best_solutions_graph(self):
        ea = self.evolutive_algorithm
        best_solutions_gen, best_solutions_exe, best_solutions_abs = ea.data_best_solutions_gen, ea.data_best_solutions_exe, ea.data_best_solutions_abs
        x = [x for x in range(0,len(best_solutions_gen))]
        return [
            {"x": x, "y": best_solutions_gen, "label": "Best: Generation",  "color": "blue" ,  "style": "-o", "markersize": 2},
            {"x": x, "y": best_solutions_exe, "label": "Best: Execution",   "color": "yellow", "style": "-", "markersize": 2},
            {"x": x, "y": best_solutions_abs, "label": "Best: Absolute",    "color": "green",  "style": ":"},
        ]
        return x, y
    

if __name__ == "__main__":
    #random.seed(0)
    instance = TSPInstanceParser.parse("./data/br17.atsp")
    ea = EvolutiveAlgorithm(instance,None)
    ea.run()
    g = Graph(instance,ea)
    g.display("best_solutions_graph")

    


    