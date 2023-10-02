import numpy as np
import math
import re
from task import Task

#returns a degree of parallelism from which splitting is reducing runtime
def min_beneficial_split(alignment_task, median_input_size, annotation_database, infra_name):
    align_model = annotation_database.runtime_estimation_model[infra_name][alignment_task.tool] 
    align_model_weight = align_model.coef_[0]
    align_model_bias = align_model.intercept_
    
    split_model = annotation_database.runtime_estimation_model[infra_name]["split_merge"]

    #estimate time it takes to split
    split_time = split_model[0] * median_input_size + split_model[1]
      
    #estimate alignment runtime without splitting
    align_time_no_split = align_model.predict(median_input_size.reshape(-1, 1))[0]
    
    #max alignment runtime after splitting to reduce runtime overall
    max_align_time_split = align_time_no_split - split_time
    
    #get input datasize for max alignment runtime after splitting and calculate min split parameter
    max_input_size_split = (max_align_time_split - align_model_bias)/align_model_weight
    min_split = math.ceil(median_input_size/max_input_size_split)

    #return ReLU of min_split, when min_split is negative, splitting increases runtime
    return min_split * (min_split > 0)


def split(DAW, annotation_database, input_description):
    try:
        alignment_task = next(task for task in DAW.tasks if task.operation == "align")
        annotation_aligner = next(aligner for aligner in annotation_database.annotation_db if aligner.toolname == alignment_task.tool)
        
    except StopIteration:
        print("Either no task with operation \"align\" was found, or there was no annotation for the alignment tool used.")
        return DAW
        
    if annotation_aligner.is_splittable == False: #if aligner does not support splitting, return DAW (no changes)
        return DAW
    
    median_input_size = np.array(0.4) #TODO: get real median input size, so far input obj of DAW is empty
    infra_name = "kubernetes-cluster" #TODO: infra may need an identifier to get corresponding entries from the annotation database?
    
    min_beneficial_split(alignment_task, median_input_size, annotation_database, infra_name)
    split_number = min_beneficial_split #TODO: implement real approach for getting number of chunks here
    
    #find splittable tasks, first is align
    first_split_task = alignment_task
    last_split_task = alignment_task
    task_splittable = True
    
    while task_splittable == True:
        output_last_split_task = re.compile(last_split_task.name + ".out_channel.*")
        next_tasks = [task for task in DAW.tasks if [requirement for requirement in task.require_input_from if output_last_split_task.match(requirement)] != []]
        if next_tasks != []:    
            for task in next_tasks:
                annotation_next_task = [annotation for annotation in annotation_database.annotation_db if annotation.toolname == task.tool]
                if annotation_next_task != []:
                    if annotation_next_task.is_splittable == True:
                        last_split_task = next_task 
                        task_splittable = True
                        continue              
                    else:
                        task_splittable = False 
                else: 
                    task_splittable = False
        else: #no next task found
            task_splittable = False       
    #TODO: find children of last splittable task
    output_last_split_task = last_split_task.name + ".out_channel." + last_split_task.outputs[0]
    child_tasks = [task for task in DAW.tasks if output_last_split_task in task.require_input_from]

    read_input_align_tool = next(input for input in first_split_task.inputs if input.input_type == "sample")
    read_input_from_DAW = first_split_task.inputs_from_DAW[first_split_task.inputs.index(read_input_align_tool)]
    split_parameter = split_number #TODO: add split param as global workflow parameter
    split_task = Task("split", "fastqsplit", [read_input_from_DAW], ["split_reads"], [], "split", "FASTQSPLIT", "/home/ninon/modules/fastqsplit.nf", input_description) 
    split_task_output = split_task.name + ".out_channel." + split_task.outputs[0]
    first_split_task.change_input(split_task_output, read_input_align_tool)
    DAW.insert_tasks(split_task)
    merge_task = Task("merge", "samtools_merge", [output_last_split_task], ["merged"], [], "merge", "SAMTOOLS_MERGE", "/home/ninon/modules/samtools_merge.nf", input_description)
    merge_task_output = merge_task.name + ".out_channel." + merge_task.outputs[0]
    for child_task in child_tasks:
        child_task.change_input(merge_task_output, output_last_split_task)
    DAW.insert_tasks(merge_task)
    
    return DAW
    
    

