
def find_alternative_tool(annotation_database):
    alt_tool_list = []
    #find tool with matching operations
    #find tool that runs with the same input/out as original
    #find tool that matches domain specific features
    # return list of mtaching tasks
    return

def is_tool_runnable(infra, input, annot):
    # check infrastructure requirements, see what runs there
    return

def choose_best_tool(list_alt_tools, annot):
    # 
    return

def replace_tool(daw, input, infrastructure, annotation):
    new_daw = daw
    for tool in daw.tasks:
        alternative_tools_list = find_alternative_tool()
        alternative_tools_list = is_tool_runnable()
        if (len(alternative_tools_list) > 1):
            final_tool = choose_best_tool()
        else:
            final_tool = tool
    return daw