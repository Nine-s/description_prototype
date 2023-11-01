nextflow.enable.dsl = 2


include { STAR_ALIGN  } from '/home/ninon/description_prototype/v1/modules_nextflow/STAR_ALIGN.nf'
include { SAMTOOLS_SORT_CONVERT  } from '/home/ninon/description_prototype/v1/modules_nextflow/SAMTOOLS.nf'
include { FASTQSPLIT  } from '/home/ninon/modules/fastqsplit.nf'
include { SAMTOOLS_MERGE  } from '/home/ninon/modules/samtools_merge.nf'

workflow{
        read_pairs_ch = Channel
            .fromPath( params.csv_input )
            .splitCsv(header: true, sep: ',')
            .map {row -> tuple(row.sample, [row.path_r1, row.path_r2])}
            .view()
        
FASTQSPLIT(read_pairs_ch)
STAR_ALIGN(FASTQSPLIT.out.split_reads, params.ref_gtf, params.ref_genome)
SAMTOOLS_MERGE(STAR_ALIGN.out.sam)
SAMTOOLS_SORT_CONVERT(SAMTOOLS_MERGE.out.merged)

}