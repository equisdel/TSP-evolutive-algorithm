# contiene la información de los arcos
# procurar un acceso rápido
import numpy as np
from Configuracion import Config

# retorna el costo del arco que va de x a y
def C(x,y):
    return Data.matrix[x,y]

# Extrae la matriz del archivo en data/p43.atsp
def extract_atsp_matrix(file_path):
  
    matrix = []
    inside_edge_weight_section = False
    
    with open(file_path, 'r') as file:
        for line in file:
           
            if 'EDGE_WEIGHT_SECTION' in line:
                inside_edge_weight_section = True
                continue

            if 'EOF' in line or 'EDGE_WEIGHT_SECTION' in line:
                break

            if inside_edge_weight_section:
                line = line.strip()
                if line:
                    row = list(map(int, line.split()))
                    matrix.append(row)
    
    return np.array(matrix)



# Recibe un archivo .atsp
class Data:

    def __init__(self, path):

        Data.atsp_path = path
        Data.matrix = extract_atsp_matrix(path)

        Config.N = Data.matrix.shape[0]

        # print(Data.matrix)

