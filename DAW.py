from task import Task

class DAW:  

    tasks:list = []
    tasks_priority:list = []
    is_scatter_gather:bool = False
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
        print("#############")
        print(tasks_list)
        for task in tasks_list:
            task_name_list.append(task.name)
        for task in tasks_list:
            for input in task.require_input_from: 
                #if what is before "out" is in task name list
                dependency_name = input.split(".out")[0] in task_name_list
                if (("out" in input) and (dependency_name in task_name_list)):
                    if (dependencies_dict[task.name] is list):
                        dependencies_dict[task.name].append(dependency_name)
                    else:
                        dependencies_dict[task.name] = []
                        dependencies_dict[task.name].append(dependency_name)
        print(dependencies_dict)
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
            #print(result)
            return result


    def define_tasks_priority(self):
        #print("###############")
        #print(self.tasks)
        tasks_dict = self.build_dict_from_dependencies(self.tasks)
        #print(tasks_dict)
        #print("###############")
        #print(tasks_dict)
        ordered_tasks_list = self.build_DAG_from_dict(tasks_dict)
        return ordered_tasks_list  #[align, sort_convert]

    # Creates a DAW object from the json description 
    def __init__(self, DAW_description, input_description, infra_description):
        # create task objects        
        tasks_list = []
        for i in range(len(DAW_description["tasks"])):
            json_task = DAW_description["tasks"][i]
            new_task = Task(json_task["name"], json_task["toolname"], json_task["inputs"], json_task["outputs"], json_task["parameters"], json_task["operation"])
            tasks_list.append(new_task)
        
        for task in tasks_list:
            task.my_print()
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

    def define_task_dependencies():
        #parse INPUT/output and write dependencies as an int that defines what should be written first
        return #task_priority #list for every task, a number corresponding to their priority

    def import_modules():
        return

    def rewrite_replace_task(self):
        return


    def to_nextflow(self):
        return

    # def rewrite_scatter_gather(self):
    #     return