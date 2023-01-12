import os
import sys
import argparse
import filetype
from pathlib import Path
from func_cvt2csv_v_1_02 import *


def run(in_path=False):
    if not in_path: 
        print("no path input!")
        sys.exit()

    in_path = Path(in_path)
    name_out = in_path.name
 
    if os.path.exists(in_path):
        if os.path.isdir(in_path): 
            cal_img_in_dir2csv(in_path, name_out) 

        elif filetype.is_image(in_path):
            cal_img2csv(in_path, name_out)

        else:
            print(in_path, "not image or directory")

    else:
        print(in_path, "not exist.")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_path', default=False, type=str, help="directory or image path")
    opt = parser.parse_args()
    return opt


def main(opt):
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)