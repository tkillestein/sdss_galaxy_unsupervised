import os, glob
from tqdm import tqdm
from utils import load_image_from_path
from scipy.ndimage import rotate
from imageio import imwrite

OUT_DIR = "./data/final_28x28_proc"

if not os.path.isdir(OUT_DIR):
    os.makedirs(os.path.join(OUT_DIR, "TRAIN"))
    os.makedirs(os.path.join(OUT_DIR, "VAL"))

# remove all galaxies without reliable PA information.
# rm ./final_64x64_unproc/glx*_0.0*

input_files = glob.glob("./data/final_28x28_unproc/*.jpg")

TRAIN_SPLIT = 0.1
split_idx = int(0.1 * len(input_files))

val_files = input_files[:split_idx]
train_files = input_files[split_idx:]

for f in tqdm(val_files):
    froot = f.split("/")[-1][:-4]  # get the root name
    pa_rot = float(froot.split("_")[-2])  # extract the required rotation

    img = load_image_from_path(f)
    rot_img = (255 * rotate(img, -pa_rot + 90, reshape=False).clip(min=0, max=1)).astype("uint8") # from 0-1 -> 0-255 for JPGs
    imwrite(os.path.join(OUT_DIR, "VAL", froot + ".jpg"), rot_img)

for f in tqdm(train_files):
    froot = f.split("/")[-1][:-4]  # get the root name
    pa_rot = float(froot.split("_")[-2])  # extract the required rotation

    img = load_image_from_path(f)
    rot_img = (255 * rotate(img, -pa_rot + 90, reshape=False).clip(min=0, max=1)).astype("uint8")
    imwrite(os.path.join(OUT_DIR, "TRAIN", froot + ".jpg"), rot_img)