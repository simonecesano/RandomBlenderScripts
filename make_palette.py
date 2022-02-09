import bpy
import sys
import os
import argparse
import json
import time
import cv2
import numpy as np
import tempfile
import re
import math
import mathutils

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []

parser = argparse.ArgumentParser(description='Reduce textures size')

parser.add_argument('materials', nargs='*', type=str, help='the materials files')

parser.add_argument('-s', '--scale')
parser.add_argument('-q', '--quality')

parser.add_argument('-c', '--clear', action='store_true')

parser.add_argument('-x', '--file_name_suffix')
parser.add_argument('-i', '--input')

parser.add_argument('-o', '--output')

args = parser.parse_args(args=arg_after_dashes())

if args.clear:
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)
        
    for obj in [ obj for obj in bpy.data.objects if obj.type == "MESH" ]:
        bpy.data.objects.remove(obj, do_unlink=True)
            
# bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    
mat_names = [ mat.name for mat in bpy.data.materials ]
if mat_names:
    print(mat_names)
else:
    print("file has no materials")

mat_count = 0
for filepath in args.materials:
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects   = [ name for name in data_from.objects if True or name.type == "MESH" ]
        data_to.materials = [ name for name in data_from.materials if not name.startswith('Dots Stroke') ]
    
    for mat in data_to.materials:
        # print(mat.name.startswith('Dots Stroke'))
        if mat is not None and (not mat.name.startswith('Dots Stroke')):
            new_name = re.sub(r'-[a-f0-9]{32,32}.+\.blend', '', os.path.basename(filepath))
            mat.name = new_name

    for obj in data_to.objects:
        if obj is not None and obj.type == "MESH":
            obj.name = obj.material_slots[0].material.name
            bpy.context.scene.collection.objects.link(obj)
            mat_count = mat_count + 1

print([ mat.name for mat in bpy.data.materials ])

# for obj in bpy.data.objects:
#     print(obj, obj.type)
#     # if obj.type != "MESH":
#     #     bpy.context.scene.collection.objects.remove(obj)

# print ('-' * 10)
# for obj in bpy.data.objects:
#     print(obj, obj.type)

# print(math.sqrt(mat_count))
# mat_count = 16
height = math.ceil(math.sqrt(mat_count))
width = math.ceil(mat_count / height)
print(width, height)

for obj in bpy.data.objects:
    print(obj, obj.type, obj.location)

i = 0
meshes = [ obj for obj in bpy.data.objects if obj.type == "MESH" ]
print(meshes)

for x in range(width):
    for y in range(height):
        print(x, y, i)
        move = mathutils.Vector((x * 12, -y * 12, 0.0))
        meshes[i].location = meshes[i].location + move

        i = i + 1
        if i >= len(meshes):
            break

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        
