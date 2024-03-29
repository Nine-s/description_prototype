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
    runtime_models = {k.lower(): annotation_database.runtime_estimation_models[k] for k in annotation_database.runtime_estimation_models}
    align_model = runtime_models[alignment_task.tool.lower()] 
    
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


def find_sample_input(DAW, channeled_inputs):
    for c_input in channeled_inputs:
        sample_input = False
        finished = False
        task = next(task for task in DAW.tasks if c_input.split(".")[0]==task.module_name)
        for i in task.inputs:
            if i.input_type=="sample":
                return c_input
            child_task_requirements = task.require_input_from
            while finished == False:
                parent_tasks = [task for task in DAW.task if task.module_name in [req.split(".")[0] for req in child_tasks_requirements]]
                #check for all parent tasks whether one of the has samples as input
                for index, p in enumerate(parent_tasks):     
                    for i in p.inputs:
                        if i.input_type=="sample":
                            return child_tasks_requirements[index]
                #otherwise: set child = parents to prepare next loop iteration
                child_tasks_requirements = []
                for p in parent_tasks:
                    child_tasks_requirements.extend(p.require_input_from)
          



def split(DAW, annotation_database, input_description):
    try:
        alignment_tasks = [task for task in DAW.tasks if task.operation == "align"]
    except StopIteration:
        print("No task with operation \"align\" was found.")
        return DAW
    
    
    for alignment_task in alignment_tasks:
        print(alignment_task.module_name)
        try:
            annotation_aligner = next(aligner for aligner in annotation_database.annotation_db if aligner.toolname.lower() == alignment_task.tool.lower())
        except StopIteration:
            print("No annotation for alignment tool " + str(alignment_task.tool) + " was found.")
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
        print(min_split)
        if((DAW.infra.number_nodes<min_split) | (min_split < 1)):
            continue
        split_number = DAW.infra.number_nodes
        DAW.wf_level_params.append(("split", split_number))
        cores = [int(node.cores) for node in DAW.infra.list_nodes] 
        
        #find splittable tasks, first is align
        first_split_task = alignment_task
        last_split_task = alignment_task
        task_splittable = True
    
        while task_splittable == True:
            output_last_split_task = re.compile(last_split_task.module_name + ".out_channel.*")
            next_tasks = [task for task in DAW.tasks if [requirement for requirement in task.require_input_from if output_last_split_task.match(requirement)] != []]
            if next_tasks != []:    
                for task in next_tasks:
                    annotation_next_task = [annotation for annotation in annotation_database.annotation_db if annotation.toolname == task.tool]
                    if annotation_next_task != []:
                        if annotation_next_task.is_splittable == True:
                            last_split_task = task 
                            task_splittable = True
                            continue              
                        else:
                            task_splittable = False 
                    else: 
                        task_splittable = False
            else: #no next task found
                task_splittable = False       

        output_last_split_task = last_split_task.module_name + ".out_channel." + last_split_task.outputs[0]
        child_tasks = [task for task in DAW.tasks if output_last_split_task in task.require_input_from]
        try:
            read_input_align_tool = next(input for input in first_split_task.inputs if input.input_type == "sample")
            read_input_channel = first_split_task.inputs_from_DAW[first_split_task.inputs.index(read_input_align_tool)]
            print(read_input_channel)
            print(read_input_align_tool)
        except StopIteration:
        #samples not direct input of align task: search along DAG to find task that provides preprocessed input
            channeled_inputs = first_split_task.require_input_from
            read_input_channel = find_sample_input(DAW, channeled_inputs)
            read_input_align_tool = read_input_channel
        split_parameter = split_number #TODO: add split param as global workflow parameter
        full_module_path = first_split_task.module_path
    
        last_slash_index = full_module_path.rfind("/")
        module_path = full_module_path[:last_slash_index]

        split_task = Task("split", "fastqsplit", [read_input_channel], ["split_reads"], [], "split", ("FASTQSPLIT_" + alignment_task.tool.upper()),  module_path + "/FASTQSPLIT.nf", input_description, {"include_from": "FASTQSPLIT"}) 
        split_task_output = split_task.module_name + ".out_channel." + split_task.outputs[0]
        first_split_task.change_input(split_task_output, read_input_align_tool)
        DAW.insert_tasks(split_task) 
        merge_task = Task("merge", "samtools_merge", [output_last_split_task], ["merged"], [], "merge", ("SAMTOOLS_MERGE_" + alignment_task.tool.upper()), module_path + "/SAMTOOLS.nf", input_description, {"channel_operators":[".collect()"], "include_from": "SAMTOOLS_MERGE"})
        merge_task_output = merge_task.module_name + ".out_channel." + merge_task.outputs[0]
        for child_task in child_tasks:
            child_task.change_input(merge_task_output, output_last_split_task)
        DAW.insert_tasks(merge_task)
    return DAW
    
    

