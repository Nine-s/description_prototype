import numpy as np
import math

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


def split(DAW, annotation_database):

    alignment_task = next(task for task in DAW.tasks if task.operation == "align")
    annotation_aligner = next(aligner for aligner in annotation_database.annotation_db if aligner.toolname == alignment_task.tool)
    if annotation_aligner.is_splittable == False: #if aligner does not support splitting, return DAW (no changes)
        return DAW
    
    median_input_size = np.array(0.4) #TODO: get real median input size, so far input obj of DAW is empty
    infra_name = "kubernetes-cluster"#TODO: infra may need an identifier to get corresponding entries from the annotation database?
    min_beneficial_split(alignment_task, median_input_size, annotation_database, infra_name)
    split_number = min_beneficial_split #TODO: implement real approach for getting number of chunks here
    DAW = DAW #TODO: implement changes in DAW object

    
    return DAW
    
    

