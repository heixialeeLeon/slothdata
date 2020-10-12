import pandas as pd
import os
import glob

CONTOURS_ID = 1056817
SHELF_ID = 1056824

def merge_csv_files(src_folder, target_csv_file):
    '''
    merge the same type csv files in the src folder to the target_csv_file
    :param src_folder:
    :param target_csv_file:
    :return:
    '''
    t_df = None
    csv_file_pattern = src_folder + "/"+"*.csv"
    for csv_file in glob.glob(csv_file_pattern):
        df = pd.read_csv(csv_file)
        if t_df is None:
            t_df = df
        else:
            t_df = t_df.append(df)
    t_df.to_csv(target_csv_file, index=False)

def merge_csv_files_with_shelf_contours(src_folder, target_csv_file):
    '''
     merge the same type csv files in the src folder to the target_csv_file, will filter the row without shelf contours
    :param src_foler:
    :param target_csv_file:
    :return:
    '''
    t_df = None
    csv_file_pattern = src_folder + "/" + "*.csv"
    for csv_file in glob.glob(csv_file_pattern):
        df = pd.read_csv(csv_file)
        if t_df is None:
            t_df = df
        else:
            t_df = t_df.append(df)
    t_df = filter_with_shelf_contours_annotation(t_df)
    t_df.to_csv(target_csv_file, index=False)

def filter_with_shelf_contours_annotation(df, contours_id=CONTOURS_ID, shelf_id = SHELF_ID):
    '''
    filter the df without the shelf contours
    :param df:
    :return:
    '''
    f_df = df[(df["ProductId"]==contours_id) | (df["ProductId"]==shelf_id)]
    return f_df

if __name__ == "__main__":
    target_csv_file = "test.csv"
    merge_csv_files_with_shelf_contours("../shelf_csv", target_csv_file)