import glob
import random
from utils.process_img import LabelmeToCoco

json_list = glob.glob("imgs/shelf_img_cut/*.json")
random.seed(1234)
random.shuffle(json_list)
N = int(len(json_list) * 0.9)

converter = LabelmeToCoco()
converter.convert(json_list[:N], "shelf_coco_train.json")
converter.convert(json_list[N:], "shelf_coco_val.json")
