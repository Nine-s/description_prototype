#!/bin/bash -ue
if [[ (unstranded == "firststrand") || (unstranded == "secondstrand") ]]; then
	STAR \
           --genomeDir . \
           --readFilesIn Mmusculus_1.fq.gz Mmusculus_2.fq.gz  \
           --runThreadN 8 \
           --outFileNamePrefix sample01. \
           --sjdbGTFfile mm9.fa \
		--alignSoftClipAtReferenceEnds No \
		--outFilterIntronMotifs RemoveNoncanonical \
		--outSAMattrIHstart 0
elif [[ unstranded == "unstranded" ]]; then
	STAR \
           --genomeDir . \
           --readFilesIn Mmusculus_1.fq.gz Mmusculus_2.fq.gz  \
		--alignSoftClipAtReferenceEnds No \
		--outSAMstrandField intronMotif \
		--outFilterIntronMotifs RemoveNoncanonical \
       	--runThreadN 8 \
       	--outFileNamePrefix sample01. \
       	--sjdbGTFfile mm9.fa \
		--outSAMattrIHstart 0
else  
	echo unstranded > error_strandness.txt
	echo "strandness cannot be determined" >> error_strandness.txt
fi
