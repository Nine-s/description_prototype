nextflow.enable.dsl = 2


include { STAR_ALIGN  } from '/home/ninon/description_prototype/v1/modules_nextflow/STAR_ALIGN.nf'
include { SAMTOOLS_SORT_CONVERT  } from '/home/ninon/description_prototype/v1/modules_nextflow/SAMTOOLS.nf'

workflow{
        read_pairs_ch = Channel
            .fromPath( params.csv_input )
            .splitCsv(header: true, sep: ',')
            .map {row -> tuple(row.sample, [row.path_r1, row.path_r2])}
            .view()
        
STAR_ALIGN(read_pairs_ch, params.ref_gtf, params.ref_genome)
SAMTOOLS_SORT_CONVERT(STAR_ALIGN.out.sam)

}