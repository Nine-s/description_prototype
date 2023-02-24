import os
import csv

class Input:  


    name:str = "sample"
    input_type:str = "reads"
    paths:str = ""
    size:float = 1
    paired:bool = True
    strand:str = "forward"
    ref_type:str = ""

    def __init__(self, name, input_type, paths, strand, ref_type):
        self.name = name
        self.input_type = input_type
        self.paths = paths
        self.strand = strand
        self.ref_type = ref_type

    # number_of_samples:int = 1
    # samples:list = []
    # references:dict = {}
#     def __init__(self, input_description):
#         # get samples
#         samples_list= []
#         nb_samples_tmp = 0
#         for i in range(len(input_description["samples"])):
#             nb_samples_tmp += 1
#             json_sample = input_description["samples"][i]
#             new_sample = Sample(json_sample)
#             samples_list.append(new_sample)
#         self.samples = samples_list
#         self.create_input_csv()
#         self.number_of_samples = nb_samples_tmp

#         #get references
#         references_dict= {}
#         for i in range(len(input_description["references"])):
#             json_ref = input_description["references"][i]
#             new_ref = Reference(json_ref)
#             references_dict[new_ref.ref_type] = new_ref
#         self.references = references_dict
#         print(references_dict)

#     # def create_input_csv(self):
#     #     # TODO: Create csv file with inputs here?
#     #     with open('input.csv', 'w') as csvfile:
#     #         filewriter = csv.writer(csvfile, delimiter=',',
#     #                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     #         filewriter.writerow(['Sample', 'path_r1', 'path_r2', 'strand'])
#     #         for sample in self.samples:
#     #                 filewriter.writerow([sample.name, sample.path_r1, sample.path_r2, sample.strand])
            

# class Sample: 

#     name:str = "sample"
#     type:str = "reads"
#     path_r1:str = ""
#     path_r2:str = ""
#     paired:bool = True
#     strand:str = "forward"
#     size:float = 1

#     def get_strand(self, strand):
#         strand_possibilities = ["forward", "reverse", "unstranded"]
#         if (strand in strand_possibilities):
#             return strand
#         else:
#             raise Exception("strand provided invalid or missing")

#     def __init__(self, sample_description): 
#         self.path_r1 = sample_description["path_r1"]
#         if (sample_description["path_r2"] != ""):
#             self.paired = True
#             self.path_r2 = sample_description["path_r2"]
#         else:
#             self.paired = False
#         self.name:str = sample_description["name"]
#         self.size = os.path.getsize(self.path_r1)
#         #todo: include size2
#         self.strand = self.get_strand(sample_description["strand"])
#         self.type = sample_description["type"]

# class Reference:  

#     name:str = ""
#     path:str = ""
#     ref_type:str = ""
#     size = 1

#     def __init__(self, description): 
#         self.name:str = description["name"]
#         self.path:int = description["path"]
#         self.ref_type:str = self.get_ref_type(description["type"])
#         self.size = os.path.getsize(self.path)
    
#     def get_ref_type(self, ref_type):
#         ref_type_possibilities = ["genome", "cdna", "gtf"] 
#         # TODO: add VCF (SNP/SNV db), and others
#         if (ref_type in ref_type_possibilities):
#             return ref_type
#         else:
#             raise Exception("ref type invalid or missing") 
