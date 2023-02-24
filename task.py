from input import Input

class Task:  

    name:str = "task_default"
    tool:str = "none"
    operation:str = "none"
    inputs:list = []
    outputs:list = []
    parameters:list = []
    require_input_from:list = [] 
    module_name:str = ""
    module_path:str = ""


    def find_module_path(self):
        #TODO
        # read library file and infer module_name and module_path
        # using the DAW description json
        return

    def create_input(self, inputs_from_DAW, input_description):
        list_inputs = []
        for input in inputs_from_DAW:
            # if ("out_channel" in input):
            #     mInput = Input(input, "sample", [sample["path_r1"], sample["path_r2"]], sample["strand"], "")
            #     list_inputs.append(mInput)
            # else:
            for sample in input_description["samples"]:
                if (sample["name"] == input):
                    mInput = Input(input, "sample", [sample["path_r1"], sample["path_r2"]], sample["strand"], "")
                    list_inputs.append(mInput)
            for reference in input_description["references"]:
                if (reference["name"] == input):
                    mInput = Input(input, "reference", [reference["path"]], "", reference["reference_type"])
                    list_inputs.append(mInput)        
        return list_inputs

    def __init__(self, name, tool, inputs_from_DAW, outputs, parameters, operation, module_name, module_path, input_description):#, require_input_from): 
        self.name:str = name
        self.tool:int = tool
        self.outputs:list = outputs
        self.parameters:list = parameters
        self.operation:str = operation
        self.module_name:str = module_name
        self.module_path:str = module_path
        inputs = self.create_input(inputs_from_DAW, input_description)
        self.inputs = inputs
        self.inputs_tasks:list = inputs_from_DAW
        require_input_from_list = []
        for input in self.inputs_tasks:        
            if (".out_channel." in input):
                require_input_from_list.append(input)
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
