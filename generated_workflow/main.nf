nextflow.enable.dsl = 2


include { STAR_ALIGN  } from /home/ninon/modules/STAR.nf
include { SAMTOOLS_SORT_CONVERT  } from /home/ninon/modules/samtools.nf

workflow{
        read_pairs_ch = Channel
            .fromPath( 'params.input_csv' )
            .splitCsv(header: true, sep: '	')
            .map {row -> tuple(row.sampleName, [row.fastq1, row.fastq2], row.strand)}
        
STAR_ALIGN(params.sample01, params.ref_gtf, params.ref_genome)
SAMTOOLS_SORT_CONVERT(align.out_channel.sam)

}