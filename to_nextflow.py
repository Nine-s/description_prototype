import pandas as pd
from itertools import chain
import os
class to_nextflow:  

    DAW = None

    def write_workflow(self, input_tasks_list):
        start = """\nworkflow{
        read_pairs_ch = Channel
            .fromPath( params.csv_input )
            .splitCsv(header: true, sep: ',')
            .map {row -> tuple(row.sample, [row.path_r1, row.path_r2])}
            .view()
        """
        #.map {row -> tuple(row.sampleName, [row.fastq1, row.fastq2], row.strand)}
        end = "\n}"
        core = self.write_core_workflow(input_tasks_list)
        return start + core + end

    def write_core_workflow(self, input_tasks_list):
        core = "\n"
        # declare strandedness env variable
        tasks = self.DAW.tasks
        for i in range(len(tasks)):
            priority_index = self.DAW.tasks_priority.index(i)
            tmp_task = tasks[priority_index]
            tmp = str(tmp_task.module_name) + "(" 
            for my_input in tmp_task.inputs_task:
                print("####")
                print(my_input)
                print(input_tasks_list)
                print("#######")
                if((".out" not in my_input) and (my_input in input_tasks_list)): 
                        tmp += "read_pairs_ch, "       
                elif((".out" not in my_input) and (my_input != "reads")):
                    tmp += "params." + my_input + ", "
                    
                else: 
                    tmp_input = my_input
                    tmp_input = tmp_input.replace("out_channel", "out")
                    tmp += tmp_input + ", "
            tmp = tmp[:-2] + ")\n"
            core += tmp
        return core
    
    # TODO: check if module path exists. Here?
    def generate_include_modules(self):
        include_string = ""
        include_dictionnary = {}
        for task in self.DAW.tasks:
            if (task.module_path in include_dictionnary):
                include_dictionnary[task.module_path].append(task.module_name)
            else:
                include_dictionnary[task.module_path] = []
                include_dictionnary[task.module_path].append(task.module_name)
        for path in include_dictionnary:
            module_names_string = ""
            for module_name in include_dictionnary[path]:
                module_names_string += module_name + " ; "
            include = "include { " + module_names_string[:-2] + " } from '" + path + "'\n"
            include_string = include_string + include
        return include_string    


    def write_docker_per_task(self):

        return

    def create_config_file(self):
        #read default manifest in resources folder
        with open("./resources/default_nextflow_config.config") as f:
            base_config = f.read()
#        with open("nextflow.config", "w"):
#            pass
        params_string = "\n\nparams {\n"
        params_string += "\tstrand = " + "'" + self.DAW.input.first_strand + "'\n"
        params_string += "\toutdir = 'results'\n"
        params_string += "\tcsv_input = './input.csv'\n"
        for i in range(len(self.DAW.tasks)):
            task_inputs = self.DAW.tasks[i].inputs
            for j in range(len(task_inputs)):
                _input = task_inputs[j]
                if ("reference" in _input.input_type):
                    params_string += "\t" + _input.name + " = '" + _input.paths[0] + "'\n"  
        for additional_param in self.DAW.wf_level_params:
            param, value = additional_param
            params_string += "\t" + param + " = " + str(value) + "\n"
        params_string += "basedir = '" + os.popen('pwd').read().strip() + "/generated_workflow'"
        params_string += "}\n"
        with open('./generated_workflow/nextflow.config', 'w') as config_file:
            config_file.write(base_config + params_string)
            config_file.close()
        #TODO: add threads #params_string += ("threads = " + str(self.DAW.infra.threads) + "\n") 
    
    def write_input_csv(self, DAW):
        mandatory_columns = ['sample', 'path_r1', 'path_r2']
        additional_columns = list(set(chain.from_iterable(list(sample.additional_columns.keys()) for sample in DAW.input.input_samples)))
        columns = mandatory_columns + additional_columns
        input_tasks_list = []
        df = pd.DataFrame(columns=columns)
        for i in range(len(DAW.input.input_samples)):
            inputDAW = DAW.input.input_samples[i]
            mandatory_values = [inputDAW.name, inputDAW.paths[0], inputDAW.paths[1]]
            additional_values = []
            for additional_element in additional_columns:
                if(additional_element in inputDAW.additional_columns):
                    additional_values.append(inputDAW.additional_columns[additional_element])
                else:
                    additional_values.append("")
            df.loc[i] = mandatory_values + additional_values
            input_tasks_list.append(inputDAW.name)
        df.to_csv("generated_workflow/input.csv", index=False)
        return input_tasks_list

    
    def __init__(self, DAW):
        self.DAW = DAW
        ### write config file
        self.create_config_file()
        # TODO add docker containers??? add entry in DAW description?
        input_tasks_list = self.write_input_csv(DAW)
        nextflow_header = "nextflow.enable.dsl = 2\n"
        include = self.generate_include_modules()
        header = nextflow_header + "\n\n" + include
        workflow = self.write_workflow(input_tasks_list)
        ##task that generate input channels
        with open("generated_workflow/main.nf", "w") as f:
            f.write("")
            f.write(header + workflow)


    def write_docker_per_task(self):
        return
