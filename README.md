# Nanopore_pipeline

An automated, reproducible workflow for gut microbiome profiling using **Oxford Nanopore 16S long-read sequencing**.  
This Snakemake pipeline integrates:

- ✅ Preprocessing (length filter + adapter trimming)  
- ✅ Taxonomic profiling with [EMU](https://github.com/treangenlab/emu)  
- ✅ Diversity analyses (alpha/beta, PERMANOVA)  
- ✅ Differential abundance (Mann–Whitney + FDR, volcano plots)  
- ✅ Core microbiome identification  
- ✅ Candidate overlap (Venn diagrams across cohorts)  

The workflow is **configurable, containerized (Conda environments auto-managed)**, and reproducible across multi-site colorectal cancer cohorts.

---

## 📦 Requirements
- [Conda](https://docs.conda.io/) (miniconda or mamba recommended)  
- [Snakemake](https://snakemake.readthedocs.io/) (≥7.0)

Install snakemake (if not installed already):
```bash
conda install -c bioconda -c conda-forge snakemake
🚀 Usage
Clone this repo:

bash
Copy code
git clone https://github.com/<your-username>/Nanopore_pipeline.git
cd Nanopore_pipeline
Place raw FASTQ files into the raw/ folder (named like barcode01.fastq.gz).

Update paths in config.yaml (especially emu_db pointing to your EMU database).

Run the workflow:

bash
Copy code
snakemake --use-conda --cores 6
📂 Folder layout
arduino
Copy code
Nanopore_pipeline/
├─ Snakefile              # Snakemake workflow
├─ config.yaml            # pipeline configuration
├─ envs/                  # per-tool conda environments
├─ scripts/               # analysis scripts
├─ metadata/              # sample metadata (TSVs)
├─ raw/                   # raw input FASTQs
└─ results/               # output (auto-created)
✨ Example Outputs
Alpha diversity plots (Shannon, Simpson, Richness)

Beta diversity (PCoA + PERMANOVA)

Volcano plots of case vs control

Core microbiome tables + Venn diagrams

Cross-cohort reproducibility summaries

🧬 Citation
If you use this workflow, please cite:
Wasim A., et al. (2025) Automated reproducible Nanopore-based pipeline for multi-cohort microbiome analysis. GitHub Repository.
