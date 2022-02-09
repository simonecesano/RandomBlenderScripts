import bpy
import sys
import os
import argparse
import json
import re
import time
import cv2
import numpy as np
import tempfile
import re

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []

parser = argparse.ArgumentParser(description='Reduce textures size')

parser.add_argument('-s', '--scale')
parser.add_argument('-q', '--quality')
parser.add_argument('-x', '--file_name_suffix')
parser.add_argument('-i', '--in_place', action='store_true')

parser.add_argument('-o', '--output')


args = parser.parse_args(args=arg_after_dashes())


def squeeze_image(file_path):
    image = cv2.imread(file_path)
    jpeg_file_path = os.path.splitext(file_path)[0] + '.jpg'
    small = cv2.resize(image, (0,0), fx=0.25, fy=0.25) 
    cv2.imwrite(jpeg_file_path, small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    return jpeg_file_path

def recurse_node_tree(node_tree, accum):
    nodes = node_tree.nodes
    for n in nodes:
        if n.type == "TEX_IMAGE":
            accum.append(n)
        if n.type == "GROUP":
            recurse_node_tree(n.node_tree, accum)

def main(args):
    nodes = []
    for mat in bpy.data.materials:
        if mat.node_tree:
            recurse_node_tree(mat.node_tree, nodes)
            
    used_images = [ n.image for n in nodes ]
    start_images = [ img for img in bpy.data.images ]
    cleanup_list = []

    for img in start_images:
        print(img.name, img in used_images)
        if img.size[0] and img.size[1] and img in used_images:
            temp_filename = tempfile.NamedTemporaryFile(prefix="tamale_", suffix='.' + img.file_format.lower()).name

            img.save_render(temp_filename)
            jpeg_filename = squeeze_image(temp_filename)

            new_img = bpy.data.images.load(jpeg_filename)
            new_img.colorspace_settings.name = img.colorspace_settings.name
        
            for n in nodes:
                if n.image == img:
                    n.image = new_img
                    if img.users == 0:                    
                        bpy.data.images.remove(img)
                    else:
                        print("image still in use")

            cleanup_list.append(temp_filename)
            cleanup_list.append(jpeg_filename)
        
    bpy.ops.file.pack_all()

    if args.in_place:
        print('saving in place')
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    elif args.output:
        print('save to ' + args.output)
        bpy.ops.wm.save_as_mainfile(filepath=args.output)
    elif args.file_name_suffix:
        
        file_name = re.sub(r'\.blend$', '-' + args.file_name_suffix + '.blend', bpy.data.filepath)
        print('save to ' + file_name)
        bpy.ops.wm.save_as_mainfile(filepath=file_name)
        
    for f in cleanup_list: os.remove(f)

# ----------------- end of main -----------------------


if not (args.in_place or args.output or args.file_name_suffix):
    print("set one of --in_place or --output or --file_name_suffix")
    print("nothing to do!")
else:
    main(args)
