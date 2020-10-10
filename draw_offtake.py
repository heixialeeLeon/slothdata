import os
import os.path as osp
import glob
import pandas as pd
import numpy as np
import cv2
import json

if not osp.exists("offtake_show"):
    os.makedirs("offtake_show")

for csv_file in glob.glob("offtake_csv/*.csv"):
    df = pd.read_csv(csv_file)
    for img_url, values in df.groupby('ImgUrl'):
        img_name = osp.split(img_url)[-1] + ".jpg"
        img = cv2.imread(osp.join("img", img_name))
        img_h, img_w = img.shape[:2]
        for ann in values.to_dict(orient='records'):
            prod = str(ann['ProductId'])
            xmin = int(round(img_w * ann['xmin']))
            ymin = int(round(img_h * ann['ymin']))
            xmax = int(round(img_w * ann['xmax']))
            ymax = int(round(img_h * ann['ymax']))
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
            cv2.putText(img, prod, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
        cv2.imwrite(osp.join("offtake_show", img_name), img)
