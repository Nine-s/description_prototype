nextflow.enable.dsl = 2


include { STAR_ALIGN  } from /home/ninon/modules/STAR.nf
include { SAMTOOLS_SORT_CONVERT  } from /home/ninon/modules/samtools.nf
include { FASTQSPLIT  } from /home/ninon/modules/fastqsplit.nf

workflow{
        read_pairs_ch = Channel
            .fromPath( 'params.input_csv' )
            .splitCsv(header: true, sep: '	')
            .map {row -> tuple(row.sampleName, [row.fastq1, row.fastq2], row.strand)}
        
FASTQSPLIT(params.sample01)
STAR_ALIGN(split.out_channel.split_reads, params.ref_gtf, params.ref_genome)
SAMTOOLS_SORT_CONVERT(align.out_channel.sam)

}