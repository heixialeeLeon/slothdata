import argparse
import os.path as osp
import os
import glob
from shutil import copyfile

parser = argparse.ArgumentParser(description="Split to small piceces")
parser.add_argument('--src', default='/home/leon/data/fix_data/need_fix2', required=False, help="the source folder")
parser.add_argument('--dest', default='/home/leon/data/fix_data/split', required=False, help="the destination folder")
args = parser.parse_args()
print(args)

SPLIT_COUNT = 500

def split(src_folder, dst_folder):
    src_pattern = osp.join(src_folder,"*.jpg")
    count = 0
    dst_folder_count = 0
    target_folder = None
    for img_file in glob.glob(src_pattern):
        # create the split dir first
        if count % SPLIT_COUNT == 0:
            target_folder= osp.join(dst_folder, str(dst_folder_count))
            dst_folder_count+=1
            os.makedirs(target_folder)
        # copy the file
        img_file_name = str(img_file).split('/')[-1]
        json_file_name = img_file_name.split('.')[0]+".json"
        target_img_file = osp.join(target_folder, img_file_name)
        target_json_file = osp.join(target_folder,json_file_name)
        copyfile(img_file, target_img_file)
        copyfile(osp.join(src_folder,json_file_name), target_json_file)
        count += 1

split(args.src, args.dest)