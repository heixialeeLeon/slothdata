import os
import os.path as osp
import glob
import pandas as pd
import numpy as np
import cv2
import json
from PIL import Image

if not osp.exists("shelf_json"):
    os.makedirs("shelf_json")

for csv_file in glob.glob("shelf_csv/*.csv"):
    df = pd.read_csv(csv_file)
    for img_url, values in df.groupby('ImageUrl'):
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
            poly = np.array(json.loads(ann['Polygon']))
            poly[:, 0] *= img_w
            poly[:, 1] *= img_h
            poly = np.round(poly).astype(np.int32)

            json_data["shapes"].append({
                "label": prod,
                "points": poly.tolist(),
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            })
        with open(osp.join("shelf_json", img_name[:-4] + ".json"), "w") as f:
            json.dump(json_data, f)
