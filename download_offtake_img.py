import os
import os.path as osp
import glob
from utils.download_img import download_img_from_csv_folder, download_img_from_csv_file

target_folder = "imgs/offtake_img"

if not osp.exists(target_folder):
    os.makedirs(target_folder)

for csv_file in glob.glob("offtake_csv/*.csv"):
    print("process : {}".format(csv_file))
    download_img_from_csv_file(csv_file, target_folder, url_key="ImgUrl")