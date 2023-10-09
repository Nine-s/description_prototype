import DAW #from DAW import add task to daw
from statistics import median

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
                daw = daw.add_compress_task("naf", task)
            elif (is_output_sam(task)):
                daw = daw.add_compress_task("cram", task)
    return daw