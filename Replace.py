from task import Task

def find_alternative_tool(annotation_db, tool_to_replace):
    alt_tool_list = []
    # print(annotation_db)
    # print(tool_to_replace)
    for tool in annotation_db:
        #find tool with matching operations
        if (tool.operation == tool_to_replace.operation):
            #find tool that runs with the same input/out as original 
            if ( input_output_matches(tool, tool_to_replace) ):
                alt_tool_list.append(tool)
    return alt_tool_list


def input_output_matches(tool, tool_to_replace):
    
    input_to_replace = tool_to_replace.mendatory_input_list
    input_tool_from_database = tool.mendatory_input_list

    output_to_replace = tool_to_replace.output_list
    output_tool_from_database = tool.output_list
    
    if ( set(input_to_replace).issubset(set(input_tool_from_database)) ):
        if ( set(output_to_replace).issubset(set(output_tool_from_database)) ):
            return True
    else:
        return False


def is_tool_runnable( tool, RAM, reference_size, model ):
    min_RAM = model.predict([[reference_size]])
    if ( RAM > min_RAM[0] + 1 ):
        return True
    else:
        return False

def choose_best_tool(list_alt_tools, annot, input_of_daw):
    # runtime
    model = annot.runtime_estimation_model
    best_tool = list_alt_tools[0]
    best_tool_predicted_runtime =  10000000#
    for tool in list_alt_tools:
        a=1
    # find tool that matches domain specific features
    return

def create_new_task(task, new_tool, input_description):
    print(task)
    name = new_tool.toolname + "_" + new_tool.operation
    tool = new_tool.toolname
    outputs = task.outputs
    parameters = 1 #TODO
    operation = new_tool.operation
    module_path = new_tool.module_path
    module_name = module_path.split("/")[-1].split(".")[0]
    inputs_from_DAW = task.inputs_from_DAW
    require_input_from_list = 1 #TODO

    new_task = Task(name=name, tool=tool, inputs_from_DAW=inputs_from_DAW, outputs=outputs, parameters=parameters, operation=operation, module_name=module_name, module_path=module_path, input_description=input_description)
    #print(self.tasks)
    new_task.my_print()
    return new_task

def replace_tool(daw, annotations, input_description, input_of_daw):

    for task in daw.tasks:
        # print("++++++")
        # print(task.tool)
        annotation_tools_list = [tool for tool in annotations.annotation_db] 
    
        # find the tool of the DAW task in the annot DB
        tool_to_replace = next((tool_in_annot for tool_in_annot in annotation_tools_list if (tool_in_annot.toolname.casefold() == task.tool.casefold())), None)
        if(tool_to_replace == None):
            print("Tool to replace not found in DB")
            continue

        # find the tools in the db that match the requirements
        alternative_tools_list = find_alternative_tool(annotations.annotation_db, tool_to_replace)
        
        if ( len(alternative_tools_list) < 1 ):
            print("No alternative found")
            continue
        else:
            # print("#### Alt tools found!")
            # for _tool in alternative_tools_list:
            #     print(_tool.toolname)
            
            RAM = daw.infra.RAM # TODO: add real values for RAM!
            reference_size = input_of_daw.size_of_reference_genome_max

            alternative_tools_list = [tool_alt for tool_alt in alternative_tools_list if (is_tool_runnable(tool_alt, RAM, reference_size, tool_alt.RAM_requirements_model))] 

            # print("#### tools with enough RAM")
            # for _tool in alternative_tools_list:
            #     print(_tool.toolname)
            
            if (len(alternative_tools_list) > 1):

                final_tool = choose_best_tool(alternative_tools_list, annotations, input_of_daw) #TODO
                final_tool = alternative_tools_list[0]
                new_task = create_new_task(task, final_tool, input_description)
                task = new_task
            else:
                continue
    return daw