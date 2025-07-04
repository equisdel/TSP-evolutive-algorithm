class Configuration:

    def __init__(self,instance_size):

        self.config = { 
            "initial population": {
                "size": Parameter("int",1000,[10,10000]), 
                "origin": Parameter("int",0,[0,instance_size]),
                "generation": ["random", "previous best"] # the first one is the default
            },
            "parent selection": {
                "mechanism": ["TS", "RBS", "FPS"],
                "probability": 0,
            },
            "crossover": {
                "mechanism": ["PMX", "OPC"],
                "probability": 0.5,
            },
            "offspring mutation": {
                "mechanism": ["flip", "default"],
                "probability": 0.15,
            },
            "survivor selection": {
                "mechanism": [""],
                "probability": 0.0,
            },
            "fitness evaluation": {
                "type": ["linear"]
            },
            "termination criteria": {
                "min generations": 100,  
                "max generations": -1,     
                "time limit_seconds": 3600, 
                "target fitness":  -1,
                "epsilon": 0.001,       
            },
            "advanced settings": {
                "automatic save": True,
                "save best N individuals": True,
                "N": 1000,
            },
        }

    def get_json_config(self):
        return self.config
    

class Parameter:

    def __init__(self,type,default,range):

        self.type = type
        self.default_value = default
        self.range = range  # a list with min-max or with all the options