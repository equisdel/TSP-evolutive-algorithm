import numpy as np

class TSPInstanceParser:
    
    @staticmethod
    def parse(file_path):
        # Parses a .atsp file and returns a TSPInstance object

        with open(file_path, 'r') as file:
            lines = file.readlines()

        name, dimension, matrix = None, None, []
        metadata = {}
        matrix_start = False

        for line in lines:
            line = line.strip()
            if line.startswith("NAME"):
                name = line.split(":")[1].strip()
            elif line.startswith("DIMENSION"):
                dimension = int(line.split(":")[1].strip())
            elif line.startswith("EDGE_WEIGHT_SECTION"):
                matrix_start = True
            elif line == "EOF":
                break
            elif matrix_start:
                row = list(map(int, line.split()))
                matrix.extend(row)

        matrix = np.array(matrix).reshape((dimension, dimension))
        return TSPInstance(name, dimension, matrix, metadata)


class TSPInstance:

    name = None
    dimension = None
    matrix = None
    metadata = None

    def __init__(self, name, dimension, matrix, metadata=None):
        self.name = name
        self.dimension = dimension
        self.matrix = matrix
        self.metadata = metadata or {}

    def get_edge_cost(self, from_city, to_city):
        return self.matrix[from_city][to_city]

    def total_cost(self, path):
        return sum(self.get_edge_cost(path[i], path[i + 1]) for i in range(len(path) - 1))
    
    def get_dimension(self):
        return self.dimension
        