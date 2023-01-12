import os
import sys
import argparse
from pathlib import Path
from func_cvt2csv_v_1_03 import *


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_path', default=False, type=str, help="directory or image path")
    parser.add_argument('-l', '--loop', default=False, type=bool, help="loop sub folder")
    opt = parser.parse_args()
    return opt


def function(in_path=False, loop=False):
    if not in_path: 
        print("no path input!")
        sys.exit()

    elif not os.path.exists(in_path):
        print(in_path, "not exist.")
        sys.exit()

    if loop and os.path.isdir(in_path): loop_folder(in_path)
    else: run(in_path)


def main(opt):
    function(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)