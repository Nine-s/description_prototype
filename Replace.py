
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
    # return list of mtaching tasks
    return alt_tool_list

def input_output_matches(tool_1, tool_2):

    return True #TODO


def is_tool_runnable( tool, RAM, reference_size, model ):
    min_RAM = model.predict([[reference_size]])
    #print(min_RAM)
    if ( RAM > min_RAM[0] + 1 ):
        return True
    else:
        return False

def choose_best_tool(list_alt_tools, annot): #TODO
    # runtime
    # find tool that matches domain specific features
    return

def replace_tool(daw, annotations):
    #print(daw.tasks)
    new_daw = daw
    for task in daw.tasks:
        annotation_tools_list = [tool for tool in annotations.annotation_db] 
        #print(annotation_tools_list)
        # print("#######")
        # print(task.tool)
        # print("########")

        tool_to_replace = next((tool_in_annot for tool_in_annot in annotation_tools_list if (tool_in_annot.toolname.casefold() == task.tool.casefold())), None)
        if(tool_to_replace == None):
            #print("Tool to replace not found in DB")
            continue
        alternative_tools_list = find_alternative_tool(annotations.annotation_db, tool_to_replace)
        if (len(alternative_tools_list)<1):
            #print("No alternative found")
            continue
        else:
            #print("OK")
            #find alternative DAW tool in annot: check if here
            RAM = daw.infra.RAM #TODO add real values for RAM!
            # TODO: add unite de mesure!
            reference_size = 2 # TODO
            alternative_tools_list = [tool_alt for tool_alt in alternative_tools_list if (is_tool_runnable(tool_alt, RAM, reference_size, tool_alt.RAM_requirements_model))]
            #print(alternative_tools_list)
            if (len(alternative_tools_list) > 1):
                final_tool = choose_best_tool(alternative_tools_list, annotations.runtime_estimation_model)
            else:
                continue #TODO
    return daw