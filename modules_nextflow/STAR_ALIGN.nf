
process STAR_ALIGN {
    label 'star'
    publishDir params.outdir

    input:
    tuple val(sample_name), path(reads)
    path(index)
    path(annotation)

    output:
    tuple val(sample_name), path("${sample_name}*.sam"), emit: sample_sam 

    shell:
    '''
    if [[ (params.strandness == "firststrand") || (params.strandedness == "secondstrand") ]]; then
		STAR \\
            --genomeDir . \\
            --readFilesIn !{reads[0]} !{reads[1]}  \\
            --runThreadN !{params.threads} \\
            --outFileNamePrefix !{sample_name}. \\
            --sjdbGTFfile !{annotation} \\
			--alignSoftClipAtReferenceEnds No \\
			--outFilterIntronMotifs RemoveNoncanonical \\
			--outSAMattrIHstart 0
	elif [[ params.strandedness == "unstranded" ]]; then
		STAR \\
            --genomeDir . \\
            --readFilesIn !{reads[0]} !{reads[1]}  \\
			--alignSoftClipAtReferenceEnds No \\
			--outSAMstrandField intronMotif \\
			--outFilterIntronMotifs RemoveNoncanonical \\
        	--runThreadN !{params.threads} \\
        	--outFileNamePrefix !{sample_name}. \\
        	--sjdbGTFfile !{annotation} \\
			--outSAMattrIHstart 0
	else  
		echo params.strandedness > error_strandness.txt
		echo "strandness cannot be determined" >> error_strandness.txt
	fi
   '''
}
