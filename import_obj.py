import bpy
import sys
import os
import argparse
import json
import re
import time
import cv2
import numpy as np

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []


parser = argparse.ArgumentParser(description='Replace/assign materials on blender file')

parser.add_argument('-f', '--material_folder')
parser.add_argument('-o', '--output')
parser.add_argument('-i', '--input')

args = parser.parse_args(args=arg_after_dashes())

folder = os.path.abspath(args.material_folder if args.material_folder else '.')
folder_name = os.path.split(folder)[-1]

file_in = args.input

imported_object = bpy.ops.import_scene.obj(filepath=file_in)

file_out = args.output if args.output else re.sub(r'\.obj$', '.blend', file_in)

print("Saving to " + file_out)

bpy.ops.file.pack_all() 
bpy.ops.wm.save_as_mainfile(filepath=file_out)        
