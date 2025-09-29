#!/usr/bin/env python3
import argparse, pandas as pd, matplotlib.pyplot as plt
from matplotlib_venn import venn2
import os

ap=argparse.ArgumentParser()
ap.add_argument("--genus-2024", required=True)
ap.add_argument("--genus-2025", required=True)
ap.add_argument("--species-2024", required=True)
ap.add_argument("--species-2025", required=True)
ap.add_argument("--out-dir", required=True)
args=ap.parse_args()

def load(f):
    df = pd.read_csv(f, sep="\t")
    if "feature" in df.columns: return set(df["feature"].astype(str))
    return set(df.iloc[:,0].astype(str))

def venn(a,b,labels,outpng):
    plt.figure(figsize=(6,6))
    venn2([a,b], set_labels=labels)
    plt.title("Candidate overlap")
    plt.savefig(outpng, dpi=150)

os.makedirs(args.out_dir, exist_ok=True)
venn(load(args.genus_2024), load(args.genus_2025), ("Genus 2024","Genus 2025"), os.path.join(args.out_dir,"venn_genus_candidates.png"))
venn(load(args.species_2024), load(args.species_2025), ("Species 2024","Species 2025"), os.path.join(args.out_dir,"venn_species_candidates.png"))
