import os
import os.path as osp
import glob
from utils.download_img import download_img_and_json_from_shelf_csv_file
from utils.process_csv import merge_csv_files_with_shelf_contours

target_folder = "imgs/shelf_img_annotation"
target_csv = "imgs/shelf_img_annotation/shelf.csv"

def download_all():
    if not osp.exists(target_folder):
        os.makedirs(target_folder)

    for csv_file in glob.glob("shelf_csv/*.csv"):
        print("process : {}".format(csv_file))
        download_img_and_json_from_shelf_csv_file(csv_file, target_folder)

def download_with_shelf_contours():
    if not osp.exists(target_folder):
        os.makedirs(target_folder)

    merge_csv_files_with_shelf_contours("shelf_csv", target_csv)
    download_img_and_json_from_shelf_csv_file(target_csv, target_folder)

if __name__ == "__main__":
    download_with_shelf_contours()