import os
import filetype
from pathlib import Path
from func_cvt2csv_v_1_02 import *

def run():
    while True:
        print("======================================================")

        in_path = input("Input filename (exit by enter): ")

        if in_path == "": 
            print("Exit program")
            break

        in_path = Path(in_path)
        name_out = in_path.name

        if os.path.exists(in_path):
            if os.path.isdir(in_path):   
                cal_img_in_dir2csv(in_path, name_out) 

            elif filetype.is_image(in_path):
                cal_img2csv(in_path, name_out)

            else:
                print(in_path, "not image or directory")
                continue
                
        else:
            print(in_path, "not exist.")


if __name__ == "__main__":
    run()