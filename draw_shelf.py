import os
import os.path as osp
import glob
import pandas as pd
import numpy as np
import cv2
import json

if not osp.exists("shelf_show"):
    os.makedirs("shelf_show")

for csv_file in glob.glob("shelf_csv/*.csv"):
    df = pd.read_csv(csv_file)
    for img_url, values in df.groupby('ImageUrl'):
        img_name = osp.split(img_url)[-1] + ".jpg"
        img = cv2.imread(osp.join("img", img_name))
        img_h, img_w = img.shape[:2]
        for ann in values.to_dict(orient='records'):
            prod = str(ann['ProductId'])
            poly = np.array(json.loads(ann['Polygon']))
            poly[:, 0] *= img_w
            poly[:, 1] *= img_h
            poly = np.round(poly).astype(np.int32)
            cv2.polylines(img, [poly], True, (0, 0, 255), 2)
            cv2.putText(img, prod, (poly[0,0], poly[0,1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
        cv2.imwrite(osp.join("shelf_show", img_name), img)
