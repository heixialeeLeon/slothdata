import pandas as pd
import urllib
import urllib.request
import os
import os.path as osp
import glob
from PIL import Image
import numpy as np
import json

def download_img_from_csv_folder(csv_folder, img_path):
    file_pattern = os.path.join(csv_folder,"*.csv")
    for csv_file in glob.glob(file_pattern):
        download_img_from_csv_file(csv_file, img_path)

def download_img_from_csv_file(csv_file, img_path, url_key="ImageUrl"):
    df = pd.read_csv(csv_file)
    urls = df[url_key].unique()
    for url in urls:
        file_name = url.split('/')[-1] + ".jpg"
        file_path = os.path.join(img_path, file_name)
        if os.path.exists(file_path):
            continue
        download_from_url(url, file_path)
    print("finish download csv: {}".format(csv_file))

def download_img_and_json_from_shelf_csv_file(csv_file, target, url_key="ImageUrl"):
    df = pd.read_csv(csv_file)
    for url, values in df.groupby(url_key):
        # download the image first
        img_name = url.split('/')[-1] + ".jpg"
        img_path = os.path.join(target, img_name)
        json_name = url.split('/')[-1] + ".json"
        json_path = os.path.join(target, json_name)

        if not os.path.exists(img_path):
            download_from_url(url, img_path)

        # download the json
        img = Image.open(img_path)
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

        with open(json_path, "w") as f:
            json.dump(json_data, f)

def download_img_and_json_from_offtake_csv_file(csv_file, img_path, url_key="ImgUrl"):
    pass

def download_from_url(url, file_name):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        get_img = response.read()
        with open(file_name, 'wb') as fp:
            fp.write(get_img)
    except:
        print('download failed')
