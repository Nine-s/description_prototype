class to_nextflow:  

    DAW = None

    def write_input_reading_task(self):
        # TODO
        return

    def write_process(self):
        # TODO
        return
    
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
            ## remove the last semi colon
            module_names_string = module_names_string[:-2]
            include = "include { " + module_names_string + " } from " + path + "\n"
            include_string = include_string + include
        return include_string    

    def declare_input_channels(self):
        ## use the "samples" section of input to declare channels
        # https://stackoverflow.com/questions/73702711/passing-list-of-filenames-to-nextflow-process
        # read_pairs_ch = channel.fromFilePairs( params.reads, checkIfExists: true ) 
        # def get_the_csv_records() {
        #     Channel
        #     .fromPath("/mnt/x/blah.csv")
        #     .splitCsv(header:true, quote: '\"')
        #     .map{ it.TheFieldIWant }
        # }
        # TODO
        return

    def write_docker_per_task(self):
        return

    def create_config_file(self):
        #read default manifest in resources folder
        with open("./resources/default_nextflow_config.config") as f:
            base_config = f.read()
        my_input = self.DAW.input
        params_string = "\n\nparams {\n"
        #TODO: add threads
        #params_string += ("threads = " + str(self.DAW.infra.threads) + "\n") 
        params_string += "outdir = 'path/to/results'\n"
        params_string += "csv_input = ./input.csv"
        if ("genome" in my_input.references.keys()):
            params_string += "genome = '" + my_input.references["genome"].path + "'\n"  
        if ("gtf" in my_input.references.keys()):
            params_string += "gtf = '" + my_input.references["gtf"].path + "'\n"  
        if ("cdna" in my_input.references.keys()):
            params_string += "cdna = '" + my_input.references["cdna"].path + "'\n"  
        with open('nextflow.config', 'w')as config_file:
            config_file.write(base_config + params_string)

    def __init__(self, DAW):
        self.DAW = DAW
        ### write config file
        self.create_config_file()
        # TODO add docker containers??? add entry in DAW description?
        
        ### write main file
        #write the header 
        nextflow_header = "nextflow.enable.dsl = 2\n"
        include = self.generate_include_modules()
        self.header = nextflow_header + "\n\n" + include
        #write the core of the workflow
        ##task that generate input channels
        ##declare the other tasks in priority order

