import pandas as pd
import urllib
import urllib.request
import os
import glob

def download_img_from_csv_folder(csv_folder, img_path):
    file_pattern = os.path.join(csv_folder,"*.csv")
    for csv_file in glob.glob(file_pattern):
        download_img_from_csv_file(csv_file, img_path)

def download_img_from_csv_file(csv_file, img_path):
    df = pd.read_csv(csv_file)
    urls = df["ImageUrl"].unique()
    for url in urls:
        file_name = url.split('/')[-1] + ".jpg"
        file_path = os.path.join(img_path, file_name)
        if os.path.exists(file_path):
            continue
        download_from_url(url, file_path)
    print("finish download csv: {}".format(csv_file))

def download_from_url(url, file_name):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        get_img = response.read()
        with open(file_name, 'wb') as fp:
            fp.write(get_img)
    except:
        print('download failed')