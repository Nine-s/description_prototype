import glob
import json
import infra
import input
from DAW import DAW
from workflow_generation import workflow
from to_nextflow import to_nextflow

with open('/home/ninon/description_prototype/v1/DAW.json') as jsonfile:
    daw_description = json.load(jsonfile)

with open('/home/ninon/description_prototype/v1/INPUT.json') as jsonfile:
    input_description = json.load(jsonfile)

with open('/home/ninon/description_prototype/v1/INFRA.json') as jsonfile:
    infra_description = json.load(jsonfile)

#define objects for infra + nodes
#my_infra = infra(infra_description)

#define objects for input + reference
#my_input = input(input_description)

# define object for DAW + task + connection
my_DAW = DAW(daw_description, input_description, infra_description)
to_nextflow(my_DAW)
#my_DAW

# # define library of tasks Nextflow(->nfcore) / CWL find repos
# my_nextflow_DAW = DAW.to_nextflow()