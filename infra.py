#class is defined using class keyword
class Infra:  

    is_cluster:bool = True
    number_nodes:int = 1
    list_nodes:list = []
    RAM:int = 1

    def __init__(self, infra_description_json): 
            list_nodes = [] 
            for node in infra_description_json["nodes"]:
                my_node = Node(node["name"], node["RAM"], node["cores"], node["CPU"])
                list_nodes.append(my_node)
            self.list_nodes:list = list_nodes
            self.RAM = list_nodes[0].ram
            if (len(list_nodes) > 1):
                self.is_cluster:bool = True
                self.number_nodes:int = len(list_nodes)
                self.bandwidth = infra_description_json["bandwidth"]
            else: 
                self.is_cluster:bool = False
                self.number_nodes:int = 1

class Node:

    name:str = ""
    ram:int = 1
    cores:int = 1
    cpu:int = 1

    def __init__(self, name, ram, cores, CPU): 
            self.name:str = name
            self.ram:int = ram
            self.cores:int = cores
            self.cpu:int = CPU #(m)
