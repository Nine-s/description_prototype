
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import json
import pandas as pd
import os


class AnnotationDB:  

    annotation_db:list = []
    rumtime_estimation_model:object = None

    @staticmethod
    def Create_runtime_estimation_model(runtime_measured):
        #TODO: edit runtime aligner with real values

        df_runtime = pd.read_csv(runtime_measured, delimiter="\t")

        # TODO: compute regressions per tool and infrastructure
        # TODO: check if relative time factors between the tools are consistant between the infrastructures
        return
        #df = pd.DataFrame({'reference_sizes': reference_sizes, 'ram_used': ram_used })
        #df.head()
        
        # X = df.iloc[:,:-1].values # feature matrix: reference_sizes
        # y = df.iloc[:,1].values # response vector: ram_used

        # # print("X")
        # # print(X)
        # # print("y")
        # # print(y)

        # model = LinearRegression()
        # model.fit(X, y)

        # ###plot
        # # plt.scatter(X, y,color='g')
        # # plt.plot(X, model.predict(X),color='k')
        # # plt.show()

        # return model
        return

    def __init__    (self, annotation_files_list):
        
        path_runtimes = "./annotation_files/runtime_aligners.csv"
        if( os.path.isfile(path_runtimes) == False):
            raise Exception("File missing: "+path_runtimes) 

        annotation_db = []
        for file_path in annotation_files_list:
            ##todo: find runtime file associated
            if ("runtime" in file_path):
                with open(file_path) as mfile:
                    self.rumtime_estimation_model = self.Create_runtime_estimation_model(mfile)
            else:
                with open(file_path) as json_file:
                    tool_annotated = ToolAnnotation(json.load(json_file))
                annotation_db.append(tool_annotated)
        self.annotation_db = annotation_db
        

class ToolAnnotation:

    toolname:str = ""
    operation:str = ""
    domain_specific_features:list = []
    is_splittable:bool = False
    mendatory_input_list:list = []
    output_list:list = []
    optional_inputs_list:list = []
    RAM_requirements_model:object = None

    @staticmethod
    def create_resource_requirements_RAM (reference_sizes, ram_used):
        df = pd.DataFrame({'reference_sizes': reference_sizes, 'ram_used': ram_used })
        df.head()
        X = df.iloc[:,:-1].values # feature matrix: reference_sizes
        y = df.iloc[:,1].values # response vector: ram_used

        # print("X")
        # print(X)
        # print("y")
        # print(y)

        model = LinearRegression()
        model.fit(X, y)

        ###plot
        # plt.scatter(X, y,color='g')
        # plt.plot(X, model.predict(X),color='k')
        # plt.show()

        return model
    
    def __init__ (self, tool_description):
        #print(tool_description)
        self.toolname = tool_description["toolname"]
        self.operation = tool_description["operation"]
        self.domain_specific_features = tool_description["domain_specific_features"]
        self.is_splittable = tool_description["is_splittable"]
        self.mendatory_input_list = tool_description["mendatory_input_list"]
        self.optional_inputs_list = tool_description["optional_inputs_list"]
        self.output_list = tool_description["output_list"]

        reference_sizes = []
        ram_used = []
        for resource_requirements in tool_description["resource_requirements_RAM"]:
            reference_sizes.append(float(resource_requirements["reference_size"]))
            ram_used.append(float(resource_requirements["RAM"].split("GB")[0])) #in GB
        self.RAM_requirements_model = self.create_resource_requirements_RAM(reference_sizes, ram_used)