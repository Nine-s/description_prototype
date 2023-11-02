workflow FASTQSPLIT{

    take:
    reads_channel 
    
    main:
    SPLIT_READS(reads_channel) \
	  	 | map { name, fastq, fastq1 -> tuple( groupKey( name, fastq.size()), fastq, fastq1 ) } \
       	 	 | transpose() \
       	 	 | map { name, fastq, fastq1 -> tuple(name, [fastq, fastq1] ) } \
       	 	 | view() \
       		 | set{ split_out }
    
    
    emit:
    split_reads = split_out
}
    
process SPLIT_READS{
  
    publishDir params.outdir
    label 'python'
    input:
    tuple val(name), path(fastq)

    output:
    tuple val(name), path("*${name}*1*.f*q"), path("*${name}*2*.f*q"), emit: split_reads

    shell:
    '''
    length=$(wc -l < !{fastq[0]})
    length=$((length / 4))
    s=$(echo !{params.split})
    z=$((length / s))
    splitby=$((${z} + 1))
    /home/simon/GitHub/workflow-kallisto-split/bin/splitFastq -i !{fastq[0]} -n ${splitby} -o !{name}_1
    /home/simon/GitHub/workflow-kallisto-split/bin/splitFastq -i !{fastq[1]} -n ${splitby} -o !{name}_2
    '''
}
