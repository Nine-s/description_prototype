#!/bin/bash -ue
if [[ (params.strand == "firststrand") || (params.strand == "secondstrand") ]]; then
	STAR \
           --genomeDir . \
           --readFilesIn MmusculusP_1.fq.gz MmusculusP_2.fq.gz  \
           --runThreadN 8 \
           --outFileNamePrefix sample02. \
           --sjdbGTFfile mm9.fa \
		--alignSoftClipAtReferenceEnds No \
		--outFilterIntronMotifs RemoveNoncanonical \
		--outSAMattrIHstart 0
elif [[ params.strand == "unstranded" ]]; then
	STAR \
           --genomeDir . \
           --readFilesIn MmusculusP_1.fq.gz MmusculusP_2.fq.gz  \
		--alignSoftClipAtReferenceEnds No \
		--outSAMstrandField intronMotif \
		--outFilterIntronMotifs RemoveNoncanonical \
       	--runThreadN 8 \
       	--outFileNamePrefix sample02. \
       	--sjdbGTFfile mm9.fa \
		--outSAMattrIHstart 0
else  
	echo params.strand > error_strandness.txt
	echo "strandness cannot be determined" >> error_strandness.txt
fi
