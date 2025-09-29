#!/usr/bin/env python3
import argparse, pandas as pd

ap=argparse.ArgumentParser()
ap.add_argument("--table", required=True)
ap.add_argument("--rank", required=True)
ap.add_argument("--abundance-threshold", type=float, default=1e-4)
ap.add_argument("--prevalence-cutoff", type=float, default=0.3)
ap.add_argument("--out", required=True)
args=ap.parse_args()

df = pd.read_csv(args.table, sep="\t", dtype=str)
df = df.set_index(df.columns[0]).apply(pd.to_numeric, errors="coerce").fillna(0.0)

n = df.shape[1]; prev_thr = args.prevalence_cutoff * n
pa = (df >= args.abundance_threshold).astype(int)
prev = pa.sum(axis=1)

core = prev[prev >= prev_thr].index
pd.DataFrame({"taxon": core}).to_csv(args.out, sep="\t", index=False)
