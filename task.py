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
    inputs_from_DAW = ""

    def create_input(self, inputs_from_DAW, input_description):
        list_inputs = []
        for input in inputs_from_DAW:
            is_input_described = False
            if(".out" in input):
                continue #TODO: check if the name before "out" exists 
            for sample in input_description["samples"]:
                if (sample["name"] == input):
                    mInput = Input(input, "sample", [sample["path_r1"], sample["path_r2"]], sample["strand"], "", sample["uncompressed_size"])
                    list_inputs.append(mInput)
                    is_input_described = True
            if(is_input_described):
                continue
            for reference in input_description["references"]:
                if (reference["name"] == input):
                    mInput = Input(input, "reference", [reference["path"]], "", reference["reference_type"], reference["uncompressed_size"])
                    list_inputs.append(mInput)   
                    is_input_described = True
            if not is_input_described:
                    raise Exception( 'The input "' + input + '" of the task '+ self.name + ' was not described in the input description file')
        return list_inputs

    def change_input(self, new_input, old_input_position):
    	old_input = self.inputs[old_input_position]
    	self.inputs.pop(old_input_position)
    	self.inputs_task[old_input_position] = new_input
    	if ".out" in new_input and new_input not in self.require_input_from:
    	    self.require_input_from.append(new_input)
    	if isinstance(old_input, str) and ".out" in old_input:
            self.require_input_from.remove(old_input)   
        
    def __init__(self, name, tool, inputs_from_DAW, outputs, parameters, operation, module_name, module_path, input_description):#, require_input_from): 
        self.name:str = name
        self.tool:str = tool
        self.outputs:list = outputs
        self.parameters:list = parameters
        self.operation:str = operation
        self.module_name:str = module_name
        self.module_path:str = module_path
        self.inputs_from_DAW = inputs_from_DAW
        inputs = self.create_input(inputs_from_DAW, input_description)
        self.inputs = inputs
        self.inputs_task:list = inputs_from_DAW
        require_input_from_list = []
        for input in self.inputs_task:        
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
