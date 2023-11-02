process SAMTOOLS_SORT_CONVERT {
    label 'samtools'
    publishDir params.outdir
    
    input:
    tuple val(sample_name), path(sam_file)
    
    output:
    tuple val(sample_name), path("${sample_name}.sorted.bam"), emit: sample_bam 
    
    script:
    """
    samtools sort ${sample_name}.bam -o ${sample_name}.sorted.bam
    """
    
}

process SAMTOOLS_MERGE {
    label 'samtools'
    publishDir params.outdir

    input:
    file out_bam
    
    output:
    tuple val("alignement_gathered.bam"), path("alignement_gathered.bam"), emit: merged
    
    script:
    """
    samtools merge alignement_gathered.bam ${out_bam}
    """
}

//samtools view -bS ${sam_file} -@ ${params.threads} | samtools sort -o ${sample_name}.sorted.bam -T tmp  -@ ${params.threads} 
