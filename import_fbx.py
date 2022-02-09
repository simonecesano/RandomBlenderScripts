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


parser = argparse.ArgumentParser(description='Imoprt FBX file"')

parser.add_argument('-f', '--material_folder')
parser.add_argument('-o', '--output')
parser.add_argument('-i', '--input')
parser.add_argument('-c', '--clear', action='store_true')
parser.add_argument('-M', '--no_materials', action='store_true')


args = parser.parse_args(args=arg_after_dashes())


if args.clear:
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)
        
    for obj in [ obj for obj in bpy.data.objects if obj.type == "MESH" ]:
        bpy.data.objects.remove(obj, do_unlink=True)


file_in = args.input

print("Opening " + file_in)

imported_object = bpy.ops.import_scene.fbx(filepath=file_in)

file_out = args.output if args.output else re.sub(r'\.fbx$', '.blend', file_in)

if args.no_materials:
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)



print("Saving to " + file_out)
# exit()
# bpy.ops.file.pack_all() 
bpy.ops.wm.save_as_mainfile(filepath=file_out)        
