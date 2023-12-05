nextflow.enable.dsl = 2


include { FASTQC  } from '/home/simon/GitHub/rnasplice_test/modules_simple/fastqc.nf'
include { TRIMGALORE  } from '/home/simon/GitHub/rnasplice_test/modules_simple/trimgalore.nf'
include { salmon ; salmon  } from '/path/salmon'
include { Hisat2 ; Hisat2  } from '/path/Hisat2'
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
        
CUSTOM_GETCHROMSIZES(params.genome)
Hisat2(params.genome, params.annotation_gtf)
DEXSEQ_ANNOTATION(params.annotation_gtf)
FASTQC(params.samples)
salmon(params.genome, params.transcripts_fasta)
GFFREAD_TX2GENE(params.annotation_gtf)
TRIMGALORE(params.samples)
salmon(TRIMGALORE.out.preprocessed_reads, SALMON_GENOMEGENERATE.out.index)
Hisat2(TRIMGALORE.out.preprocessed_reads, STAR_GENOMEGENERATE.out.index, params.annotation_gtf)
SAMTOOLS(STAR_ALIGN.out.sam)
MERGE_RESULTS_SALMON(SALMON_QUANT.out.transcripts.collect())
DEXSEQ_COUNT(SAMTOOLS.out.bam, DEXSEQ_ANNOTATION.out.gff, params.alignment_quality)
MERGE_RESULTS_DEXSEQ(DEXSEQ_COUNT.out.dexseq_clean_txt.collect())
DEXSEQ_EXON(MERGE_RESULTS_DEXSEQ.out.clean_counts, DEXSEQ_ANNOTATION.out.gff, params.csv_input, params.csv_contrastsheet, params.n_dexseq_plot)
BEDTOOLS_GENOMECOV(SAMTOOLS.out.bam)
TXIMPORT(MERGE_RESULTS_SALMON.out.gathered_bam, GFFREAD_TX2GENE.out.tx2gene)
BEDCLIP_FORWARD(BEDTOOLS_GENOMECOV.out.bedgraph_forward, CUSTOM_GETCHROMSIZES.out.sizes)
BEDCLIP_REVERSE(BEDTOOLS_GENOMECOV.out.bedgraph_reverse, CUSTOM_GETCHROMSIZES.out.sizes)
DRIMSEQ_FILTER(TXIMPORT.out.txi_dtu, TXIMPORT.out.tximport_tx2gene, params.csv_input, params.min_samps_gene_expr, params.min_samps_feature_expr, params.min_samps_feature_prop, params.min_feature_expr, params.min_feature_prop, params.min_gene_expr)
BEDGRAPH_TO_BIGWIG_REVERSE(BEDCLIP_REVERSE.out.bedgraph, CUSTOM_GETCHROMSIZES.out.sizes)
BEDGRAPH_TO_BIGWIG_FORWARD(BEDCLIP_FORWARD.out.bedgraph, CUSTOM_GETCHROMSIZES.out.sizes)
DEXSEQ_DTU(DRIMSEQ_FILTER.out.drimseq_samples_tsv, DRIMSEQ_FILTER.out.drimseq_counts_tsv, params.csv_contrastsheet, params.n_dexseq_plot)

}