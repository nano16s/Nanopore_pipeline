#!/usr/bin/env python3
import argparse, numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

ap=argparse.ArgumentParser()
ap.add_argument("--table", required=True)
ap.add_argument("--metadata", required=True)
ap.add_argument("--group", required=True)
ap.add_argument("--case-label", required=True)
ap.add_argument("--control-label", required=True)
ap.add_argument("--out-prefix", required=True)
args=ap.parse_args()

tbl = pd.read_csv(args.table, sep="\t", dtype=str)
tbl = tbl.set_index(tbl.columns[0]).apply(pd.to_numeric, errors="coerce").fillna(0.0)
tbl = tbl.T  # samples in rows
meta = pd.read_csv(args.metadata, sep="\t", dtype=str).set_index("sample_id")

ids = tbl.index.intersection(meta.index)
tbl, meta = tbl.loc[ids], meta.loc[ids]

case = tbl[meta[args.group]==args.case_label]
ctrl = tbl[meta[args.group]==args.control_label]

rows=[]
for feat in tbl.columns:
    a, b = case[feat].values, ctrl[feat].values
    log2fc = np.log2((a.mean()+1e-6)/(b.mean()+1e-6))
    try: _, p = mannwhitneyu(a,b)
    except: p=1.0
    rows.append([feat, log2fc, p])

res = pd.DataFrame(rows, columns=["feature","log2fc","p"])
res["q"] = multipletests(res["p"], method="fdr_bh")[1]
res.to_csv(args.out_prefix+"_diff.tsv", sep="\t", index=False)

# volcano
plt.figure(figsize=(7,6))
plt.scatter(res["log2fc"], -np.log10(res["p"]), c="grey", alpha=0.6)
sig = res["q"] < 0.1
plt.scatter(res.loc[sig,"log2fc"], -np.log10(res.loc[sig,"p"]), c="red")
plt.axhline(-np.log10(0.05), ls="--", c="black")
plt.axvline(1, ls="--", c="black"); plt.axvline(-1, ls="--", c="black")
plt.xlabel("log2FC (case/control)"); plt.ylabel("-log10 p")
plt.title("Differential abundance")
plt.tight_layout(); plt.savefig(args.out_prefix+"_volcano.png", dpi=150)
