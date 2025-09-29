#!/usr/bin/env python3
import argparse, pandas as pd, matplotlib.pyplot as plt
from skbio.stats.ordination import pcoa
from skbio.diversity import beta_diversity
from skbio.stats.distance import permanova

ap = argparse.ArgumentParser()
ap.add_argument("--table", required=True)
ap.add_argument("--metadata", required=True)
ap.add_argument("--group", required=True)
ap.add_argument("--out-prefix", required=True)
args = ap.parse_args()

# read
df = pd.read_csv(args.table, sep="\t", dtype=str)
df = df.set_index(df.columns[0]).apply(pd.to_numeric, errors="coerce").fillna(0.0).T
meta = pd.read_csv(args.metadata, sep="\t", dtype=str).set_index("sample_id")

ids = df.index.intersection(meta.index)
df, meta = df.loc[ids], meta.loc[ids]

# distance + ordination
dm = beta_diversity("braycurtis", df.values, ids)
ord_res = pcoa(dm)

coords = ord_res.samples[["PC1","PC2"]]
coords.to_csv(args.out_prefix + "_pcoa_coordinates.tsv", sep="\t")

perm = permanova(dm, grouping=meta[args.group], permutations=999)
with open(args.out_prefix + "_permanova.txt","w") as f: f.write(str(perm)+"\n")

# plot
plt.figure(figsize=(6,6))
for g in meta[args.group].unique():
    ix = meta[meta[args.group]==g].index
    plt.scatter(coords.loc[ix,"PC1"], coords.loc[ix,"PC2"], label=g)
plt.xlabel(f"PC1 ({ord_res.proportion_explained['PC1']:.1%})")
plt.ylabel(f"PC2 ({ord_res.proportion_explained['PC2']:.1%})")
plt.legend(); plt.title(f"PCoA Bray–Curtis by {args.group}")
plt.tight_layout(); plt.savefig(args.out_prefix + "_pcoa.png", dpi=300)
