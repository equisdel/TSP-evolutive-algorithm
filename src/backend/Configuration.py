class Configuration:

    MS = 10   # default population size

    def __init__(self,instance_size):

        self.config = {         # todos los parámetros se inicializan con el valor por defecto
            "initialization": {
                "mechanism":        Parameter("array",  0,      ["random"]),
                "population size":  Parameter("int",    self.MS,[10,10000]), 
                "city of origin":   Parameter("int",    0,      [0,instance_size]),
            },
            "parent selection": {
                "mechanism":        Parameter("array",  0,      ["TS", "RBS", "FPS"]),
                "probability":      Parameter("prob",   0,      [0,1]),
            },
            "crossover": {
                "mechanism":        Parameter("array",  0,      ["PMX","OPC"]),
                "probability":      Parameter("prob",   0.5,    [0,1])
            },
            "offspring mutation": {
                "mechanism":        Parameter("array",  0,      ["flip", "default"]),
                "probability":      Parameter("prob",   0.15,   [0,1]),
            },
            "survivor selection": {
                "mechanism":        Parameter("array",  0,      ["generational"]),
                "probability":      Parameter("prob",   0.0,    [0,1]),
            },
            "fitness evaluation": {
                "type":             Parameter("array",  0,      ["linear"])
            },
            "termination criteria": {
                "min generations":  Parameter("int",    100,    [1,1000]),  
                "max generations":  Parameter("int",    -1,     [-1,100000]),     
                "time limit [s]":   Parameter("int",    -1,     [-1,3600]), 
                "target fitness":   Parameter("int",    -1,     [-1,1e9]),
                "epsilon":          Parameter("float",  0.001,  [-1,100]),       
            },
            "advanced settings": {
                "automatic save":   Parameter("bool",   True,   [True,False]),  
                "save best N":      Parameter("bool",   True,   [True,False]),
                "N":                Parameter("int",    min(500,self.MS),   [0,self.MS]),
            },
        }

    def get_json_config(self):
        return self.config
    
    def display_json_config(self):
        for x in self.config:
            for y in self.config[x]:
                print(y," - ",self.config[x][y].get_value())
    
    def update_parameter(self,section_name,param_name,value):
        self.config[section_name][param_name].set_value(value) 

class Parameter:

    def __init__(self,type,default,range):
        self.type = type
        self.default = default
        self.range = range      # a list with min-max or with all the options
        self.value = default

    def get_type(self):
        return self.type

    def get_default(self):
        return self.default

    def get_range(self):
        return self.range

    def get_value(self):
        if self.type == "array":
            return self.range[self.value]
        else:
            return self.value

    def get_index(self):
        if self.type == "array":
            return self.value
        else: 
            print("Error: no es de tipo array")
            return -1
        
    def set_value_to_default(self):
        self.value = self.default
    
    def _format_value(self,value):
        if self.type == "int":
            return int(value)
        elif self.type == "float" or self.type == "prob":
            return float(value)
        else: 
            return value

    def set_value(self, value):
        print(value)
        formated_value = self._format_value(value)
        if self.validate(formated_value):
            self.value = formated_value
        else: 
            print("Valor fuera de rango! Debe estar dentro de:"+self.range)

    def validate(self,value):
        # additional checking in case frontend checking fails
        print("validation",value,"range",self.range)
        if self.type == "int":
            print(isinstance(value, (int)))
            return isinstance(int(value), (int)) and self.range[0] <= value <= self.range[1]
        elif self.type == "prob":
            return isinstance(value, (int, float)) and 0.0 <= value <= 1.0
        elif self.type == "bool":
            return value == True or value == False
        elif self.type == "array":
            print("??",self.range)
            return 0 <= value < len(self.range)
