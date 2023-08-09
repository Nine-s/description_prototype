import os
import pathlib 
import csv

class Input:  


    name:str = "sample"
    input_type:str = "reads"
    paths = []
    size:float = 1
    paired:bool = True
    strand:str = "forward"
    ref_type:str = ""
    uncompressed_size:int = 1 #GB

    def __init__(self, name, input_type, paths, strand, ref_type, uncompressed_size):
        self.name = name
        possible_input_types = ["sample", "reference"]
        self.uncompressed_size = uncompressed_size
        if not (input_type in possible_input_types): raise Exception( 'The variable "input_type" should be either "sample" or "reference"')
        else: self.input_type = input_type

        for path in paths:
            if not (os.path.exists(path)): raise Exception( 'The input file provided ' + path + ' does not exist') 
        self.paths = paths
        
        possible_strand_types = ["forward", "reverse", "unstranded"]

        possible_ref_types = ["genome", "annotation", "others"]
        

        if (input_type=="sample"):
            if (strand not in possible_strand_types): 
                raise Exception( 'The variable "strand" should be "forward", "reverse" or "unstranded", not '+strand)
            else:
                self.strand = strand

        elif (input_type=="reference"):
            
            if not (ref_type in possible_ref_types): raise Exception( 'The variable "strand" should be "genome", "annotation" or "others"')
            self.ref_type = ref_type
            strand = ""
            
        