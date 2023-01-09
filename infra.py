#class is defined using class keyword
class infra:  

    _is_cluster:bool = True
    _number_nodes:int = 1
    _list_nodes:list = []

    @property
    def is_cluster(self):
        return type(self)._is_cluster
    @is_cluster.setter
    def is_cluster(self, value):
        type(self)._is_cluster = bool(value)

    @property
    def number_nodes(self):
        return type(self)._number_nodes
    @number_nodes.setter
    def number_nodes(self, value):
        type(self)._number_nodes = int(value)

    @property
    def list_nodes(self):
        return type(self)._list_nodes
    @list_nodes.setter
    def list_nodes(self, value):
        type(self)._list_nodes = list(value)

    def __init__(self,is_cluster,number_nodes, list_nodes): 
            self.is_cluster:bool = is_cluster
            self.number_nodes:int = number_nodes
            self.list_nodes:list = list_nodes

    #user defined function of class
    def func(self):
            print("After calling func() method..")
            print("My dog's name is", self.name)
            print("His color is", self.color)

class nodes:  

    _name:str = ""
    _ram:int = 1

    @property
    def name(self):
        return type(self)._name
    @name.setter
    def name(self, value):
        type(self)._name = str(value)

    @property
    def ram(self):
        return type(self)._ram
    @ram.setter
    def ram(self, value):
        type(self)._ram = list(value)


    def __init__(self,name,ram): 
            self.name:str = name
            self.ram:int = ram

    def func(self):
            print("After calling func() method..")
            print("My dog's name is", self.name)
            print("His color is", self.color)

