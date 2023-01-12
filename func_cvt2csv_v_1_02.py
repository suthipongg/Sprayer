import os
import cv2
import filetype
from pathlib import Path
import time
import csv


def check_csv_name(dir_path, name_out):
    ls_file = os.listdir(dir_path)
    n = 1
    new_name_out = name_out
    while True:
        if new_name_out+'.csv' in ls_file:
            new_name_out = name_out + "_" + str(n)
            n += 1
        
        else: return new_name_out + '.csv'


def cal_img_in_dir2csv(dir_path, name_out):
    ls_img = os.listdir(dir_path)
    n_img = len(ls_img)
    start_time_global = time.time()
    start_time_local = start_time_global
    name_out = check_csv_name(dir_path, name_out)

    with open(dir_path / name_out, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)

        for n, filename in enumerate(ls_img):
            img = dir_path / filename
            if os.path.isdir(img): continue

            if filetype.is_image(img):
                per = round(calculateData(str(img)), 2)
                writer.writerow([filename, per])
                
                compute_time = round((time.time() - start_time_local)*1000)
                print(str(round(n/n_img*100))+'%', compute_time, "ms.", filename, ":", per)

                start_time_local = time.time()

    all_time = time.time()-start_time_global

    if all_time > 1: 
        print("========= run time in this folder:", round(all_time, 2), "s. =========")
    else: 
        print("========= run time in this folder:", round(all_time*1000), "ms. =========")


def cal_img2csv(img_path, name_out):
    img_name = Path(img_path).name
    start_time = time.time()
    name_out = check_csv_name(img_path.parent, os.path.splitext(name_out)[0])
    
    with open(img_path.parent / name_out, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        per = round(calculateData(str(img_path)), 2)
        writer.writerow([img_name, per])
        file_csv.close()
        
    compute_time = round((time.time() - start_time)*1000)
    print(compute_time, "ms.", img_name, ":", per)


def calculateData(file):
    im = cv2.imread(file)
    w, h, d = im.shape
    black = sum(im.flatten() < 255)
    return black / (w * h * d) * 100