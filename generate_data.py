import os
import pandas as pd
from utils import *
from multiprocessing import Pool
import argparse
from itertools import repeat
from tqdm.auto import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("nproc", type=int, help="Number of processes to use", default=5)
parser.add_argument("out_dir", type=str, help="Location to write files to", default="./")
parser.add_argument("ldmin", type=float, help="Minimum LD25 value to use", default=0.8)
parser.add_argument("ldmax", type=float, help="Maximum LD25 value to use", default=1.3)

args = parser.parse_args()
N_PROC = args.nproc
out_dir = args.out_dir
ldmin = args.ldmin
ldmax = args.ldmax

res = pd.read_csv("./hyperleda.csv")
print("{} records ingested".format(res.shape[0]))

# apply some basic cuts
mask = ((res.logD25 > ldmin) & (res.logD25 < ldmax) & (res.OType == "G")).values
print("Selected {} galaxies".format(mask.sum()))
res_trim = res.iloc[mask].fillna("NA")
morphtypes = res_trim.MType.values != "NA"
print("{} with morphological information".format(morphtypes.sum()))


def generate_cutout_stamp(dfrow, out_dir, imgsize=64, pad_factor=1.2, verbose=True):
    i, row = dfrow
    rotang = row.PA if row.PA != "NA" else 0
    filename = "glx_{}_{:.1f}_{}.jpg".format(row.PGC, rotang, row.MType)
    ps = compute_optimal_platescale(imgsize, row.logD25, pad_factor)
    out_loc = os.path.join(out_dir, filename)
    _ = get_sdss_stamp(row.ra, row.dec, ps, imgsize, out_loc, verbose=verbose)

    return None


if N_PROC == 1:
    for dfrow in tqdm(res_trim.iterrows(), total=res_trim.shape[0], desc="Generating data"):
        generate_cutout_stamp(dfrow, out_dir=out_dir)
else:
    print("beginning query run with {} threads".format(N_PROC))
    with Pool(N_PROC) as pool:
        pool.starmap(generate_cutout_stamp, zip(res_trim.iterrows(), repeat(out_dir)))

print("done!")
