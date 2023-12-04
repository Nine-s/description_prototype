nextflow.enable.dsl = 2


include { FASTQC  } from '/home/simon/GitHub/rnasplice_test/modules_simple/fastqc.nf'
include { TRIMGALORE  } from '/home/simon/GitHub/rnasplice_test/modules_simple/trimgalore.nf'
include { SALMON_GENOMEGENERATE  } from '/home/simon/GitHub/rnasplice_test/modules_simple/salmon_genome_generate.nf'
include { SALMON_QUANT  } from '/home/simon/GitHub/rnasplice_test/modules_simple/salmon.nf'
include { STAR_GENOMEGENERATE  } from '/home/simon/GitHub/rnasplice_test/modules_simple/star_genome_generate.nf'
include { STAR_ALIGN  } from '/home/simon/GitHub/rnasplice_test/modules_simple/star_align.nf'
include { SAMTOOLS  } from '/home/simon/GitHub/rnasplice_test/modules_simple/samtools.nf'
include { CUSTOM_GETCHROMSIZES  } from '/home/simon/GitHub/rnasplice_test/modules_simple/getchromsizes.nf'
include { BEDTOOLS_GENOMECOV  } from '/home/simon/GitHub/rnasplice_test/modules_simple/bedtoolsgenomecov.nf'
include { BEDCLIP as BEDCLIP_FORWARD; BEDCLIP as BEDCLIP_REVERSE } from '/home/simon/GitHub/rnasplice_test/modules_simple/bedclip.nf'
include { BEDGRAPHTOBIGWIG as BEDGRAPH_TO_BIGWIG_FORWARD; BEDGRAPHTOBIGWIG as BEDGRAPH_TO_BIGWIG_REVERSE } from '/home/simon/GitHub/rnasplice_test/modules_simple/bedgraphtobigwig.nf'
include { DEXSEQ_ANNOTATION  } from '/home/simon/GitHub/rnasplice_test/modules_simple/dexseq_annotation.nf'
include { DEXSEQ_COUNT  } from '/home/simon/GitHub/rnasplice_test/modules_simple/dexseq_count.nf'
include { MERGE_RESULTS_DEXSEQ  } from '/home/simon/GitHub/rnasplice_test/modules_simple/merge_results_dexseq.nf'
include { DEXSEQ_EXON  } from '/home/simon/GitHub/rnasplice_test/modules_simple/dexseq_exon.nf'
include { GFFREAD_TX2GENE  } from '/home/simon/GitHub/rnasplice_test/modules_simple/gffread_tx2gene.nf'
include { MERGE_RESULTS_SALMON  } from '/home/simon/GitHub/rnasplice_test/modules_simple/merge_results.nf'
include { TXIMPORT  } from '/home/simon/GitHub/rnasplice_test/modules_simple/tximport.nf'
include { DRIMSEQ_FILTER  } from '/home/simon/GitHub/rnasplice_test/modules_simple/drimseq_filter.nf'
include { DEXSEQ_DTU  } from '/home/simon/GitHub/rnasplice_test/modules_simple/dexseq_dtu.nf'

workflow{
        read_pairs_ch = Channel
            .fromPath( params.csv_input )
            .splitCsv(header: true, sep: ',')
            .map {row -> tuple(row.sample, [row.path_r1, row.path_r2])}
            .view()
        
DEXSEQ_ANNOTATION(params.annotation_gtf)
STAR_GENOMEGENERATE(params.genome, params.annotation_gtf)
CUSTOM_GETCHROMSIZES(params.genome)
GFFREAD_TX2GENE(params.annotation_gtf)
TRIMGALORE(read_pairs_ch)
SALMON_GENOMEGENERATE(params.genome, params.transcripts_fasta)
FASTQC(read_pairs_ch)
STAR_ALIGN(TRIMGALORE.out.preprocessed_reads, STAR_GENOMEGENERATE.out.index, params.annotation_gtf)
SALMON_QUANT(TRIMGALORE.out.preprocessed_reads, SALMON_GENOMEGENERATE.out.index)
MERGE_RESULTS_SALMON(SALMON_QUANT.out.transcripts.collect())
SAMTOOLS(STAR_ALIGN.out.sam)
TXIMPORT(MERGE_RESULTS_SALMON.out.gathered_bam, GFFREAD_TX2GENE.out.tx2gene)
DEXSEQ_COUNT(SAMTOOLS.out.bam, DEXSEQ_ANNOTATION.out.gff, params.alignment_quality)
MERGE_RESULTS_DEXSEQ(DEXSEQ_COUNT.out.dexseq_clean_txt.collect())
DRIMSEQ_FILTER(TXIMPORT.out.txi_dtu, TXIMPORT.out.tximport_tx2gene, params.csv_input, params.min_samps_gene_expr, params.min_samps_feature_expr, params.min_samps_feature_prop, params.min_feature_expr, params.min_feature_prop, params.min_gene_expr)
BEDTOOLS_GENOMECOV(SAMTOOLS.out.bam)
BEDCLIP_FORWARD(BEDTOOLS_GENOMECOV.out.bedgraph_forward, CUSTOM_GETCHROMSIZES.out.sizes)
DEXSEQ_DTU(DRIMSEQ_FILTER.out.drimseq_samples_tsv, DRIMSEQ_FILTER.out.drimseq_counts_tsv, params.csv_contrastsheet, params.n_dexseq_plot)
BEDGRAPH_TO_BIGWIG_FORWARD(BEDCLIP_FORWARD.out.bedgraph, CUSTOM_GETCHROMSIZES.out.sizes)
DEXSEQ_EXON(MERGE_RESULTS_DEXSEQ.out.clean_counts, DEXSEQ_ANNOTATION.out.gff, params.csv_input, params.csv_contrastsheet, params.n_dexseq_plot)
BEDCLIP_REVERSE(BEDTOOLS_GENOMECOV.out.bedgraph_reverse, CUSTOM_GETCHROMSIZES.out.sizes)
BEDGRAPH_TO_BIGWIG_REVERSE(BEDCLIP_REVERSE.out.bedgraph, CUSTOM_GETCHROMSIZES.out.sizes)

}