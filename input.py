
class input:  

    _number_of_samples:int = 1
    _samples:list = []

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

class samples:  

    _size:float = 1
    _strandedness:str = "forward"
    _paired:bool = True

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


class references:  

    _name:bool = True
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

