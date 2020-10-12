import os
import os.path as osp
import glob
import tqdm
from utils.process_img import cut_img_and_json


img_path = "imgs/offtake_img"

if not osp.exists("imgs/offtake_img_cut"):
    os.makedirs("imgs/offtake_img_cut")

for img_path in tqdm.tqdm(glob.glob("imgs/offtake_img/*.jpg")):
    cut_img_and_json(img_path, "imgs/offtake_img_cut", "tblr")
