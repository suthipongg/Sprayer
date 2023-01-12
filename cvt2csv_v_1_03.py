import os
from pathlib import Path
from func_cvt2csv_v_1_03 import *


def function():
    while True:
        print("======================================================")
        in_path = input("Input filename (exit by enter): ")
        if in_path == "": 
            print("Exit program")
            break
        elif not os.path.exists(in_path):
            print(in_path, "not exist.")
            continue

        while True:
            loop = input("Do you want to loop sub folder? Y/n[]: ")

            if loop.lower() in ["y", "yes"]: loop = True
            elif loop.lower() in ["n", "no"]:
                loop = False
                print("Not loop folder")
            else:
                print("Please type Y/n")
                continue

            break

        if loop and os.path.isdir(in_path): loop_folder(in_path)
        else: run(in_path)


if __name__ == "__main__":
    function()