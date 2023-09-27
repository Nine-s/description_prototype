
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import json
import pandas as pd
import os


class AnnotationDB:  

    annotation_db:list = []
    runtime_estimation_model:object = None

    @staticmethod
    def create_runtime_estimation_model(runtime_measured):
        #TODO: add kallisto when completed

        df_runtime = pd.read_csv(runtime_measured, delimiter=",")
        aligners = (df_runtime.columns[2:])

        infrastructures = df_runtime["infrastructure"].unique()

        list_models = []
        for infra in infrastructures: 
            df_infra = df_runtime.loc[df_runtime["infrastructure"] == infra]
            this_infra = []
            for aligner in aligners:
                df = pd.DataFrame({'reference_sizes': df_infra["dataset_size"], 'runtime': df_infra[aligner] })
                X = df.iloc[:,:-1].values # feature matrix: reference_sizes
                y = df.iloc[:,1].values # response vector: ram_used
                model = LinearRegression()
                model.fit(X, y)
                #plt.scatter(X, y)
                #plt.plot(X, model.predict(X))

                this_infra.append(model)
            #plt.show()
            list_models.append(this_infra)
        return list_models

    def __init__    (self, annotation_files_list):
        
        path_runtimes = "./annotation_files/runtime_aligners.csv"
        if( os.path.isfile(path_runtimes) == False):
            raise Exception("File missing: "+path_runtimes) 
        else:
            with open(path_runtimes) as mfile:
                self.runtime_estimation_model = self.create_runtime_estimation_model(mfile)
        annotation_db = []
        for file_path in annotation_files_list:
            with open(file_path) as json_file:
                #print(file_path)
                tool_annotated = ToolAnnotation(json.load(json_file))
            annotation_db.append(tool_annotated)
        self.annotation_db = annotation_db
        

class ToolAnnotation:

    toolname:str = ""
    operation:list = []
    domain_specific_features:list = []
    is_splittable:bool = False
    mendatory_input_list:list = []
    output_list:list = []
    #optional_inputs_list:list = []
    RAM_requirements_model:object = None

    @staticmethod
    def create_resource_requirements_RAM (reference_sizes, ram_used):
        df = pd.DataFrame({'reference_sizes': reference_sizes, 'ram_used': ram_used })
        df.head()
        X = df.iloc[:,:-1].values # feature matrix: reference_sizes
        y = df.iloc[:,1].values # response vector: ram_used

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
        #self.optional_inputs_list = tool_description["optional_inputs_list"]
        self.output_list = tool_description["output_list"]
        self.module_path =  tool_description["module_path"]
        reference_sizes = []
        ram_used = []
        for resource_requirements in tool_description["resource_requirements_RAM"]:
            reference_sizes.append(float(resource_requirements["reference_size"]))
            ram_used.append(float(resource_requirements["RAM"].split("GB")[0])) #in GB
        self.RAM_requirements_model = self.create_resource_requirements_RAM(reference_sizes, ram_used)