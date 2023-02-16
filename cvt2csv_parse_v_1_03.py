import os
import sys
import argparse
from func_cvt2csv_v_1_03 import *


def function(path=False, loop=False, save=False):
    if not path: 
        print("no path input!")
        sys.exit()

    elif not os.path.exists(path):
        print(path, "not exist.")
        sys.exit()

    if loop and os.path.isdir(path): 
        if not os.path.isdir(path):
            print("This path not directory, can't search sub folder")
            run(path, save)
        else:
            loop_folder(path, save)
    else: 
        run(path, save)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default=False, type=str, help="directory or image path")
    parser.add_argument('-l', '--loop', default=False, action='store_true', help="loop sub folder")
    parser.add_argument('-s', '--save', default=False, action='store_true', help="save file result as csv type")
    opt = parser.parse_args()
    return opt


def main(opt):
    function(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)