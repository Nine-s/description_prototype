import DAW #from DAW import add task to daw
from statistics import median
from task import Task


def create_compress_task(compression_type, task):
    print(task)
    operation = "compression"
    name = compression_type + "_" + operation
    if (compression_type == "naf"):
        tool = "X" #TODO
        outputs = ""
    elif (compression_type == "cram"):
        tool = "X" #TODO
        outputs = ""#
    module_path = "./nextflow_modules/" + compression_type + ".nf"
    module_name = module_path.split("/")[-1].split(".")[0]
    #outputs = task.outputs
    parameters = 1 #TODO
    operation = operation
    inputs_from_DAW = task.inputs_from_DAW
    require_input_from_list = 1 #TODO

    new_task = Task(name=name, tool=tool, inputs_from_DAW=inputs_from_DAW, outputs=outputs, parameters=parameters, operation=operation, module_name=module_name, module_path=module_path, input_description=input_description)
    #print(self.tasks)
    new_task.my_print()
    return new_task

def is_output_fastq(task):
    if ('fastq' in task.output):
        return True
    else:
        return False
    
def is_output_sam(task):
    if ('sam' in task.output):
        return True
    else:
        return False

def compress_before_file_transfer(daw): 
    if (daw.infra.iscluster == False):
        return daw
    else:
        for task in daw.tasks:
            print(task.outputs)
            if ( median(daw.input.sizes_of_samples) < "1G"):
                continue
            elif( is_output_fastq(task)):    
                new_task = create_compress_task("naf", task)
            elif (is_output_sam(task)):
                new_task = create_compress_task("cram", task)
    # TODO: change input of child tasks to output of new_task
    # child_tasks = [task for task in daw.tasks if output_last_split_task in task.require_input_from]
    
    # TODO: add decompress task
    
    daw.insert_tasks(new_task)
    return daw