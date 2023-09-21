
from sklearn.linear_model import LinearRegression
from scipy.optimize import nnls
from matplotlib import pyplot as plt
import json
import pandas as pd
import os


class AnnotationDB:  

    annotation_db:list = []
    runtime_estimation_model:object = None


    @staticmethod
    def Create_alignment_runtime_estimation_model(runtime_measured):
        #TODO: add kallisto when completed

        df_runtime = pd.read_csv(runtime_measured, delimiter=",")
        aligners = (df_runtime.columns[2:])

        infrastructures = df_runtime["infrastructure"].unique()

        list_models = {}
        for infra in infrastructures: 
            df_infra = df_runtime.loc[df_runtime["infrastructure"] == infra]
            this_infra = {}
            for aligner in aligners:
                df = pd.DataFrame({'reference_sizes': df_infra["dataset_size"], 'runtime': df_infra[aligner] })
                X = df.iloc[:,:-1].values # feature matrix: reference_sizes
                y = df.iloc[:,1].values # response vector: time_used
                model = LinearRegression(positive=True)
                model.fit(X, y)
                #plt.scatter(X, y)
                #plt.plot(X, model.predict(X)
                this_infra[aligner] = model
            #plt.show()
            list_models[infra] = this_infra
        return list_models

    @staticmethod
    def Create_split_runtime_estimation_model(runtime_measured):

        df_runtime = pd.read_csv(runtime_measured, delimiter=",")

        infrastructures = df_runtime["infrastructure"].unique()

        list_models = {}
        for infra in infrastructures: 
            df_infra = df_runtime.loc[df_runtime["infrastructure"] == infra]
            df = pd.DataFrame({'reference_sizes': df_infra["dataset_size"], 'runtime': df_infra["duration"] })
            X = df.iloc[:,:-1].values # feature matrix: reference_sizes
            y = df.iloc[:,1].values # response vector: time_used
            
            #use nnls for non-negative weights
            model = nnls(X, y)
            model = (model[0][0], model[1])
            
            list_models[infra] = model
        return list_models



    def __init__    (self, annotation_files_list):
        
        path_runtimes_align = "./annotation_files/runtime_aligners.csv"
        if( os.path.isfile(path_runtimes_align) == False):
            raise Exception("File missing: "+path_runtimes_align) 
        else:
            with open(path_runtimes_align) as mfile:
                self.runtime_estimation_model = self.Create_alignment_runtime_estimation_model(mfile)  
                 
        path_runtimes_split = "./annotation_files/runtime_split_merge.csv"
        if( os.path.isfile(path_runtimes_split) == False):
            raise Exception("File missing: "+path_runtimes_split) 
        else:
            with open(path_runtimes_split) as mfile:
                split_estimators = self.Create_split_runtime_estimation_model(mfile)   
        for infra in split_estimators:
        	self.runtime_estimation_model[infra]["split_merge"] = split_estimators[infra]                          
        annotation_db = []        
        for file_path in annotation_files_list:
            with open(file_path) as json_file:
                print(file_path)                

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

        reference_sizes = []
        ram_used = []
        for resource_requirements in tool_description["resource_requirements_RAM"]:
            reference_sizes.append(float(resource_requirements["reference_size"]))
            ram_used.append(float(resource_requirements["RAM"].split("GB")[0])) #in GB
        self.RAM_requirements_model = self.create_resource_requirements_RAM(reference_sizes, ram_used)
