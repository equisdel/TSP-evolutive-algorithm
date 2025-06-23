import json

class Log:

    base_path = "./logs/"

    def __init__(self):
        return None
    
    def write(cls,ea):
        # given evolutive algorithm it will load the data into the log
        global base_path
        instance = ea.instance
        path = base_path + "/" + instance.name
        print("path is: ",path)
        last_execution = {
            "info": {
                "id": 0,
                "start_time": "",
                "end_time": "",
                "ending_trigger": "",  # e.g., "convergency", "manual", "unknown"
                "total_generations": "",
                "diversity": ""
            },
            "instance": {
                "id": "",
                "name": "example_instance_name",
                "size": 100,
                "description": ""
            },
            "algorithm": {
                "initial_population": {"method": "", "reference": ""},
                "mechanisms": {
                    "parent_selection": {},
                    "survivor_selection": {},
                    "crossover": {},
                    "mutation": {}
                },
                "probabilities": {"mutation": "", "crossover": ""},
                "convergency": {
                    "convergency_time": "",
                    "min_generations": "",
                    "epsilon": ""
                }
            },
            "history": {
                "best_solutions_gen": [],
                "best_solutions_exe": [],
                "best_solutions_abs": [],
                "best_generation": {
                    "best_individual": {},
                    "all_individuals": {}
                }
            }
        }

        json.dump(last_execution)
        # json.write lalala path

        # it is relational, clearly, then for ML you will manage