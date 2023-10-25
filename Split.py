from task import Task
import numpy as np
import math
import re
import pandas as pd
import statistics
from sklearn.preprocessing import PolynomialFeatures



#returns a degree of parallelism from which splitting is reducing runtime
def min_beneficial_split(alignment_task, annotation_database, median_input_size, ram, cpu, ref_size):
    poly = PolynomialFeatures(degree=2)
    align_scaler = annotation_database.sandardscaler
    align_model = annotation_database.runtime_estimation_models[alignment_task.tool] 
    
    wf_characteristics = pd.DataFrame({'dataset_size': [(median_input_size)],
                                    'RAM': [(ram)], 
                                    'CPUMHz': [(cpu)], 
                                    'ref_genome_size': [(ref_size)] })

    normalized_wf_characteristics = align_scaler.transform(wf_characteristics)
    wf_characteristics_poly = poly.fit_transform(wf_characteristics)
    wf_characteristics_poly = poly.transform(normalized_wf_characteristics)
    
    align_time_no_split = align_model.predict(wf_characteristics_poly)

    
    split_model = annotation_database.runtime_estimation_models["split_merge"]
    split_scaler = annotation_database.split_merge_scaler
    
    normalized_wf_characteristics = split_scaler.transform(wf_characteristics)
    wf_characteristics_poly = poly.fit_transform(wf_characteristics)
    wf_characteristics_poly = poly.transform(normalized_wf_characteristics)
    
    split_time = split_model.predict(wf_characteristics_poly)

    
    #max alignment runtime after splitting to reduce runtime overall
    max_align_time_split = align_time_no_split - split_time
    
    #search for split param from where predicted alignment time is beneficial considering the newly added split time
    for i in range(1,100):
        input_size_chunked = median_input_size/i
        updated_wf_characteristics = pd.DataFrame({'dataset_size': [(input_size_chunked)],
                                    'RAM': [(ram)], 
                                    'CPUMHz': [(cpu)], 
                                    'ref_genome_size': [(ref_size)] })
        normalized_wf_characteristics = align_scaler.transform(updated_wf_characteristics)
        wf_characteristics_poly = poly.fit_transform(updated_wf_characteristics)
        wf_characteristics_poly = poly.transform(normalized_wf_characteristics)
    
        align_time_chunked = align_model.predict(wf_characteristics_poly)
        if(align_time_chunked < max_align_time_split):
            return i 
            
    return 0
    
    
    #return ReLU of min_split, when min_split is negative, splitting increases runtime


def split(DAW, annotation_database, input_description):
    try:
        alignment_task = next(task for task in DAW.tasks if task.operation == "align")
        annotation_aligner = next(aligner for aligner in annotation_database.annotation_db if aligner.toolname == alignment_task.tool)
    except StopIteration:
        print("Either no task with operation \"align\" was found, or there was no annotation for the alignment tool used.")
        return DAW
        
    if annotation_aligner.is_splittable == False: #if aligner does not support splitting, return DAW (no changes)
        return DAW

    median_input_size = statistics.median(DAW.input.size_of_samples)
    ram = DAW.infra.RAM
    cpus = [node.cpu for node in DAW.infra.list_nodes]
    for i, element in enumerate(cpus):
        cpus[i] = int(element.replace("m",""))
    cpu = statistics.median(cpus)
    ref_size = DAW.input.size_of_reference_genome_max
    
    min_split = min_beneficial_split(alignment_task, annotation_database, median_input_size, ram, cpu, ref_size)
    if(DAW.infra.number_nodes<min_split):
        return DAW
    split_number = DAW.infra.number_nodes
    DAW.wf_level_params.append(("split", split_number))
    cores = [int(node.cores) for node in DAW.infra.list_nodes] 
    thread_number = int(statistics.median(cores))
    DAW.wf_level_params.append(("threads", thread_number))

    
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
    
    

