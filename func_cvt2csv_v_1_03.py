import os
import cv2
import filetype
from pathlib import Path
import time
import csv


def extract_name(file_name):
    file_name = os.path.splitext(file_name)[0]
    if len(file_name) < 7: file_name = "       "
    model = file_name[:2]
    rate = file_name[3:5]
    speed = file_name[5]
    altitude = file_name[6]
    cm = file_name.split('_')
    if len(cm) < 2: 
        return [model, rate, speed, altitude, ""]
    elif len(cm[1]) < 3: 
        return [model, rate, speed, altitude, ""]
    cm = cm[1][:3]
    return [model, rate, speed, altitude, cm]


def check_csv_name(dir_path, name_out):
    ls_file = os.listdir(dir_path)
    n = 1
    new_name_out = name_out
    while True:
        if new_name_out+'.csv' in ls_file:
            new_name_out = name_out + "_" + str(n)
            n += 1
        
        else: 
            return new_name_out + '.csv'


def cal_img_in_dir2csv(dir_path, save_result):
    name_out = dir_path.name
    ls_img = os.listdir(dir_path)
    n_img = len(ls_img) - 1
    start_time_global = time.time()
    start_time_local = start_time_global
    name_out = check_csv_name(dir_path, name_out)

    non = 1
    opened = 0
    for n, filename in enumerate(ls_img):
        if opened == 0 and save_result:
            file_csv = open(dir_path / name_out, 'w', newline='')
            writer = csv.writer(file_csv)
            writer.writerow(["File name", "Model (L)", "Rate (L/rai)", "Speed (m/s)", 
                                "Altitude (m)", "Distance (cm)", "dense (%)"])
            opened = 1
        
        img = dir_path / filename
        if os.path.isdir(img): continue

        if filetype.is_image(img):
            non = 0
            dense = round(calculateData(str(img)), 2)

            extract = extract_name(filename)
            if opened:
                writer.writerow([filename]+extract+[dense])
            
            compute_time = round((time.time() - start_time_local)*1000)
            print(f"{str(round(n/n_img*100))}% {compute_time} ms. {filename} (model {extract[0]}L, rate {extract[1]}, speed {extract[2]}, altitude {extract[3]}, distance {extract[4]}cm) : {dense}%")
            start_time_local = time.time()

    if opened:
        file_csv.close()

    if non: 
        print("No image!")
        if opened:
            os.remove(file_csv.name)

    all_time = time.time()-start_time_global

    if all_time > 1: 
        print("========== run time in this folder:", round(all_time, 2), "s. ==========")
    else: 
        print("========== run time in this folder:", round(all_time*1000), "ms. ==========")


def cal_img2csv(img_path, save_result):
    img_name = img_path.name
    start_time = time.time()
    name_out = check_csv_name(img_path.parent, os.path.splitext(img_name)[0])
    dense = round(calculateData(str(img_path)), 2)
    
    if save_result:
        file_csv = open(img_path.parent / name_out, 'w', newline='')
        writer = csv.writer(file_csv)
        writer.writerow(["File name", "Model (L)", "Rate (L/rai)", "Speed (m/s)", 
                            "Altitude (m)", "Distance (cm)", "dense (%)"])
        extract = extract_name(img_name)
        writer.writerow([img_name]+extract+[dense])
        file_csv.close()
        
    compute_time = round((time.time() - start_time)*1000)
    print(f"{compute_time} ms. {img_name} (model {extract[0]}L, rate {extract[1]}, speed {extract[2]}, altitude {extract[3]}, distance {extract[4]}cm) : {dense}%")


def calculateData(file):
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray.shape
    threshould_value = 179
    threshould = cv2.threshold(gray, threshould_value, 255,cv2.THRESH_BINARY_INV)[1]
    bin_img_threshould = 1 - (threshould / 255.0)
    threshould_dense = round(sum(bin_img_threshould.flatten() == 0)/ (w*h) * 100, 2)
    return threshould_dense


def run(in_path, save_result):
    in_path = Path(in_path)
 
    if os.path.isdir(in_path): 
        cal_img_in_dir2csv(in_path, save_result) 

    elif filetype.is_image(in_path, save_result):
        cal_img2csv(in_path)

    else:
        print(in_path, "not image or directory")


def loop_folder(in_path, save):
    for (root,dirs,files) in os.walk(in_path, topdown=True):
        print(f"<<<<<<<<<<<<<<<<<<<<<<{root}>>>>>>>>>>>>>>>>>>>>>>")
        run(root, save)