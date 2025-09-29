import glob
import os
import yaml

configfile: "config.yaml"

RAW_DIR = config["raw_dir"]
FILT_DIR = config["filtered_dir"]
TRIM_DIR = config["trimmed_dir"]
EMU_DIR  = config["emu_dir"]
COMB_DIR = config["combined_dir"]
ANALYSIS = config["analysis_dir"]
CANDS    = config["candidates_dir"]
THREADS  = int(config["threads"])

SAMPLES = sorted([os.path.basename(x).replace(".fastq.gz","")
                  for x in glob.glob(config["samples_glob"])])

rule all:
    input:
        expand(f"{EMU_DIR}/{{s}}.tsv", s=SAMPLES),
        config["emu_combined_genus"]["2024"],
        config["emu_combined_genus"]["2025"],
        config["emu_combined_species"]["2024"],
        config["emu_combined_species"]["2025"],
        f"{ANALYSIS}/core_2024_genus.tsv",
        f"{ANALYSIS}/core_2025_genus.tsv",
        f"{ANALYSIS}/venn_core_genus_2024_vs_2025.png",
        f"{ANALYSIS}/genus_batch_pcoa.png",
        f"{ANALYSIS}/genus_batch_permanova.txt",
        f"{ANALYSIS}/species_batch_pcoa.png",
        f"{ANALYSIS}/species_batch_permanova.txt",
        f"{ANALYSIS}/genus_batch_alpha.tsv",
        f"{ANALYSIS}/species_batch_alpha.tsv",
        f"{ANALYSIS}/genus_cohort_diff.tsv",
        f"{ANALYSIS}/species_cohort_diff.tsv",
        f"{CANDS}/venn_genus_candidates.png",
        f"{CANDS}/venn_species_candidates.png"

rule length_filter:
    input: f"{RAW_DIR}/{{sample}}.fastq.gz"
    output: f"{FILT_DIR}/{{sample}}.fastq.gz"
    conda: "envs/seqkit.yaml"
    shell:
        "mkdir -p {FILT_DIR} && seqkit seq -m {config[length_min]} -M {config[length_max]} {input} | pigz -c > {output}"

rule porechop:
    input: f"{FILT_DIR}/{{sample}}.fastq.gz"
    output: f"{TRIM_DIR}/{{sample}}_trimmed.fastq"
    conda: "envs/porechop.yaml"
    shell:
        "mkdir -p {TRIM_DIR} && porechop -i {input} --format fastq.gz -o {output}"

rule emu:
    input: f"{TRIM_DIR}/{{sample}}_trimmed.fastq"
    output: f"{EMU_DIR}/{{sample}}.tsv"
    conda: "envs/emu.yaml"
    threads: THREADS
    shell:
        "mkdir -p {EMU_DIR} && emu abundance --db {config[emu_db]} --threads {threads} --output-dir {EMU_DIR} --output-basename {wildcards.sample} {input}"
