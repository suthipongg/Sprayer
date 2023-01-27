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
    n_img = len(ls_img) - 1
    start_time_global = time.time()
    start_time_local = start_time_global
    name_out = check_csv_name(dir_path, name_out)

    with open(dir_path / name_out, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        non = 1
        
        for n, filename in enumerate(ls_img):
            img = dir_path / filename
            if os.path.isdir(img): continue

            if filetype.is_image(img):
                non = 0
                dense = round(calculateData(str(img)), 2)
                
                writer.writerow([filename, dense])
                
                compute_time = round((time.time() - start_time_local)*1000)
                print(str(round(n/n_img*100))+'%', compute_time, "ms.", filename, ":", dense)

                start_time_local = time.time()

        file_csv.close()
        
        if non: 
            print("No image!")
            os.remove(file_csv.name)

    all_time = time.time()-start_time_global

    if all_time > 1: 
        print("========== run time in this folder:", round(all_time, 2), "s. ==========")
    else: 
        print("========== run time in this folder:", round(all_time*1000), "ms. ==========")


def cal_img2csv(img_path, name_out):
    img_name = Path(img_path).name
    start_time = time.time()
    name_out = check_csv_name(img_path.parent, os.path.splitext(name_out)[0])
    
    with open(img_path.parent / name_out, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        dense = round(calculateData(str(img_path)), 2)
        writer.writerow([img_name, dense])
        file_csv.close()
        
    compute_time = round((time.time() - start_time)*1000)
    print(compute_time, "ms.", img_name, ":", dense)


def calculateData(file):
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray.shape
    threshould_value = 179
    threshould = cv2.threshold(gray, threshould_value, 255,cv2.THRESH_BINARY_INV)[1]
    bin_img_threshould = 1 - (threshould / 255.0)
    threshould_dense = round(sum(bin_img_threshould.flatten() == 0)/ (w*h) * 100, 2)
    return threshould_dense


def run(in_path):
    in_path = Path(in_path)
    name_out = in_path.name
 
    if os.path.isdir(in_path): 
        cal_img_in_dir2csv(in_path, name_out) 

    elif filetype.is_image(in_path):
        cal_img2csv(in_path, name_out)

    else:
        print(in_path, "not image or directory")


def loop_folder(in_path):
    ls_folder = os.listdir(in_path)
    for dir in ls_folder:
        file_path = Path(in_path) / dir
        if os.path.isdir(file_path):
            loop_folder(file_path)

    print(f"<<<<<<<<<<<<<<<<<<<<<<{in_path}>>>>>>>>>>>>>>>>>>>>>>")
    run(in_path)