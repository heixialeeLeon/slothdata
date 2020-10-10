import os
import os.path as osp
import glob
import pandas as pd
import numpy as np
import cv2
import json
from PIL import Image

if not osp.exists("offtake_json"):
    os.makedirs("offtake_json")

for csv_file in glob.glob("offtake_csv/*.csv"):
    df = pd.read_csv(csv_file)
    for img_url, values in df.groupby('ImgUrl'):
        img_name = osp.split(img_url)[-1] + ".jpg"
        img = Image.open(osp.join("img", img_name))
        img_w, img_h = img.size

        json_data = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": img_name,
            "imageData": None,
            "imageHeight": img_h,
            "imageWidth": img_w
        }
        for ann in values.to_dict(orient='records'):
            prod = str(ann['ProductId'])
            xmin = int(round(img_w * ann['xmin']))
            ymin = int(round(img_h * ann['ymin']))
            xmax = int(round(img_w * ann['xmax']))
            ymax = int(round(img_h * ann['ymax']))
            
            json_data["shapes"].append({
                "label": prod,
                "points": [[xmin, ymin], [xmax, ymax]],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            })
        with open(osp.join("offtake_json", img_name[:-4] + ".json"), "w") as f:
            json.dump(json_data, f)
