from task import Task
from input import Input
from infra import Infra

class DAW:  

    tasks:list = []
    tasks_priority:list = []
    is_scatter_gather:bool = False
    input:Input = None
    infra:Infra = None
    # _tasks:list = []
    # _tasks_priority:list = []
    # _is_scatter_gather:bool = False

    # @property
    # def tasks(self):
    #     return type(self)._tasks
    # @tasks.setter
    # def tasks(self, value):
    #     type(self)._tasks = list(value)

    # @property
    # def tasks_priority(self):
    #     return type(self)._tasks_priority
    # @tasks_priority.setter
    # def tasks_priority(self, value):
    #     type(self)._tasks_priority = list(value)

    @staticmethod
    def build_dict_from_dependencies(tasks_list):
        dependencies_dict = {}
        #get names of tasks
        task_name_list = []        
        for task in tasks_list:
            task_name_list.append(task.name)
        for task in tasks_list:            
            for input in task.require_input_from:                 
                if (".out_channel." in input):
                    dependency_name = input.split(".out")[0]
                    #if dependency name is in task list
                    if(dependency_name in task_name_list):
                        if (dependency_name in dependencies_dict):
                            dependencies_dict[dependency_name].append(task.name)
                        else:
                            dependencies_dict[dependency_name] = []
                            dependencies_dict[dependency_name].append(task.name)
                    else:
                        raise Exception("error: " + dependency_name+ " is not declared in " + str(input))                      
        return dependencies_dict

    @staticmethod
    def build_DAG_from_dict(dependencies_dict):
        #https://stackoverflow.com/questions/42195291/topological-sort-kahns-algorithm-trouble
        # Find number of incoming edges for each vertex
        in_degree = {}
        for x, neighbors in dependencies_dict.items():
            in_degree.setdefault(x, 0)
            for n in neighbors:
                in_degree[n] = in_degree.get(n, 0) + 1
        # Iterate over edges to find vertices with no incoming edges
        empty = {v for v, count in in_degree.items() if count == 0}
        result = []
        while empty:
            # Take random vertex from empty set
            v = empty.pop()
            result.append(v)
            # Remove edges originating from it, if vertex not present
            # in adjacency list use empty list as neighbors
            for neighbor in dependencies_dict.get(v, []):
                in_degree[neighbor] -= 1
                # If neighbor has no more incoming edges add it to empty set
                if in_degree[neighbor] == 0:
                    empty.add(neighbor)
        if len(result) != len(in_degree):
            return None # Not DAG
        else:
            return result

    def define_tasks_priority(self):
        tasks_dict = self.build_dict_from_dependencies(self.tasks)
        ordered_tasks_list = self.build_DAG_from_dict(tasks_dict)
        return ordered_tasks_list

    # Creates a DAW object from the json description 
    def __init__    (self, DAW_description, input_description, infra_description):
        # create task objects
        self.infra = infra_description
        self.input = Input(input_description)      
        tasks_list = []
        for i in range(len(DAW_description["tasks"])):
            json_task = DAW_description["tasks"][i]
            new_task = Task(json_task["name"], json_task["toolname"], json_task["inputs"], json_task["outputs"], json_task["parameters"], json_task["operation"], json_task["module_name"], json_task["module_path"])
            tasks_list.append(new_task)
        self.tasks = tasks_list
        # define their priority
        self.tasks_priority = self.define_tasks_priority() #define
    

    # Uses infra and input objects to understand IF the workflow should be rewritten and how
    def rewriting_DAWs(self, input, infra):
        old_tasks_priority = self.tasks_priority()
        old_tasks = self.tasks()
        for task_index in range(len(old_tasks)):
            if (self.tasks[task_index].operation == "aligner"):
                return

        #self.tasks, DAW.tasks_priority = rewrite_DAW(self, infra, input)

    def my_print(self):
        print("DAW")
        print(str(self.name))
        print(str(self.tool))
        print(str(self.inputs))
        print(str(self.outputs))
        print(str(self.parameters))
        print(str(self.operation))
        print(self.require_input_from)
    # def rewrite_scatter_gather(self):
    #     return