class Task:  

    name:str = "task_default"
    tool:str = "none"
    operation:str = "none"
    inputs:list = []
    outputs:list = []
    parameters:list = []
    require_input_from:list = [] 

    def __init__(self, name, tool, inputs, outputs, parameters, operation):#, require_input_from): 
        self.name:str = name
        self.tool:int = tool
        self.inputs:list = inputs
        self.outputs:list = outputs
        self.parameters:list = parameters
        self.operation:str = operation
        require_input_from_list = []
        for input in inputs:
            if (input[1]=="channel"):
                require_input_from_list.append(input[0])
        self.require_input_from:list = require_input_from_list #build_task_dependencies(require_input_from)

    def my_print(self):
        print("TASK")
        print(str(self.name))
        print(str(self.tool))
        print(str(self.inputs))
        print(str(self.outputs))
        print(str(self.parameters))
        print(str(self.operation))
        print(self.require_input_from)

    # def build_nextflow(self):
    #     task_name 
    #     task_label
    #     input
    #     output
    #     script
    #     basecommand
    #     parameters
    
    # def build_CWL(self):
    #     print("After calling func() method..")
    #     print("My dog's name is", self.name)
    #     print("His color is", self.color)


# class inputs:  

# class outputs:

# class parameters:


    # _name:str = "task_default"
    # _tool:str = "none"
    # _operation:str = "none"
    # _inputs:list = []
    # _outputs:list = []
    # _parameters:list = []
    # _require_input_from:list = [] 

    # @property
    # def name(self):
    #     return type(self)._name
    # @name.setter
    # def name(self, value):
    #     type(self)._name = str(value)

    # @property
    # def tool(self):
    #     return type(self)._tool
    # @tool.setter
    # def tool(self, value):
    #     type(self)._tool = str(value)

    # @property
    # def inputs(self):
    #     return type(self)._inputs
    # @inputs.setter
    # def inputs(self, value):
    #     type(self)._inputs = list(value)

    # @property
    # def outputs(self):
    #     return type(self)._outputs
    # @outputs.setter
    # def outputs(self, value):
    #     type(self)._outputs = list(value)

    # @property
    # def parameters(self):
    #     return type(self)._parameters
    # @parameters.setter
    # def parameters(self, value):
    #     type(self)._parameters = list(value)

    # @property
    # def require_input_from(self):
    #     return type(self)._require_input_from
    # @require_input_from.setter
    # def require_input_from(self, value):
    #     type(self)._require_input_from = list(value)
