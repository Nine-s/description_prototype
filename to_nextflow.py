class to_nextflow:  

    DAW = None

    def write_workflow(self):
        start = """\n
        read_pairs_ch = Channel
            .fromPath( 'params.input_csv' )
            .splitCsv(header: true, sep: '\t')
            .map {row -> tuple(row.sampleName, [row.fastq1, row.fastq2], row.strand)}
        """
        end = "\n}"
        core = self.write_core_workflow()
        return start + core + end

    def write_core_workflow(self):
        core = "\n"
        tasks = self.DAW.tasks
        for i in range(len(tasks)):
            priority_index = self.DAW.tasks_priority.index(i)
            tmp_task = tasks[priority_index]
            #print(tmp_task.my_print()) 
            # add channel.out
            #tmp = str(tmp_task.name) + "(" + str([str(e.name) for e in tmp_task.inputs]) + ")\n"
            tmp = str(tmp_task.name) + "(" 
            #TODO: in task.py/DAW.py: chech if upward task exists
            for my_input in tmp_task.inputs_tasks:
                if((".out" not in my_input) and (my_input != "reads")):
                    tmp += "params." + my_input + ", "
                else: 
                    tmp += my_input + ", "
            tmp = tmp[:-2] + ")\n"
            core += tmp
        #print(core)
        return core
    
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
            include = "include { " + module_names_string[:-2] + " } from " + path + "\n"
            include_string = include_string + include
        return include_string    


    def write_docker_per_task(self):
        return

    def create_config_file(self):
        #read default manifest in resources folder
        with open("./resources/default_nextflow_config.config") as f:
            base_config = f.read()
        with open("nextflow.config", "w"):
            pass
        params_string = "\n\nparams {\n"
        params_string += "outdir = 'results'\n"
        params_string += "csv_input = ./input.csv \n"
        for i in range(len(self.DAW.tasks)):
            task_inputs = self.DAW.tasks[i].inputs
            for j in range(len(task_inputs)):
                _input = task_inputs[j]
                if ("reference" in _input.input_type):
                    params_string += _input.ref_type + " = '" + _input.paths[0] + "'\n"  
        with open('nextflow.config', 'a') as config_file:
            config_file.write(base_config + params_string)
        #TODO: add threads #params_string += ("threads = " + str(self.DAW.infra.threads) + "\n") 
    
    
    def __init__(self, DAW):
        self.DAW = DAW
        ### write config file
        self.create_config_file()
        # TODO add docker containers??? add entry in DAW description?
        
        nextflow_header = "nextflow.enable.dsl = 2\n"
        include = self.generate_include_modules()
        header = nextflow_header + "\n\n" + include
        workflow = self.write_workflow()
        ##task that generate input channels
        with open("generated_workflow/main.nf", "w") as f:
            f.write("")
            f.write(header + workflow)

