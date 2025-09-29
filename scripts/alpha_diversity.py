#!/usr/bin/env python3
import argparse, numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, kruskal

def shannon(p): nz=p[p>0]; return -(nz*np.log(nz)).sum()
def gini_simpson(p): return 1.0 - np.sum(p**2)

ap=argparse.ArgumentParser()
ap.add_argument("--table", required=True)
ap.add_argument("--metadata", required=True)
ap.add_argument("--group", required=True)
ap.add_argument("--out-prefix", required=True)
args=ap.parse_args()

df = pd.read_csv(args.table, sep="\t", dtype=str)
X = df.set_index(df.columns[0]).apply(pd.to_numeric, errors="coerce").fillna(0.0).T
meta = pd.read_csv(args.metadata, sep="\t", dtype=str).set_index("sample_id")
ids = X.index.intersection(meta.index)
X, meta = X.loc[ids], meta.loc[ids]

P = X.div(X.sum(axis=1).replace(0,np.nan), axis=0).fillna(0.0)
alpha = pd.DataFrame({
    "shannon": P.apply(lambda r: shannon(r.values), axis=1),
    "gini_simpson": P.apply(lambda r: gini_simpson(r.values), axis=1),
    "observed_richness": (X > 0).sum(axis=1),
}, index=P.index)

for m in alpha.columns:
    plt.figure()
    alpha[m].groupby(meta[args.group]).plot(kind="box")
    plt.title(f"{m} by {args.group}")
    plt.savefig(args.out_prefix+f"_{m}.png")
