import bpy
import sys
import os
import argparse
import json
import re

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []

parser = argparse.ArgumentParser(description='Rebder Blender file')

parser.add_argument('-c', '--clear', action='store_true')
parser.add_argument('-a', '--assign', action='store_true')

parser.add_argument('-r', '--resolution_percentage')

parser.add_argument('-f', '--output_format')
parser.add_argument('-q', '--exit_after_render')

args = parser.parse_args(args=arg_after_dashes())

bpy.context.scene.render.filepath = bpy.data.filepath.replace('.blend', '.png')
bpy.context.scene.render.resolution_percentage = int(args.resolution_percentage) if args.resolution_percentage else 100 

bpy.ops.render.render(write_still = True)


if args.exit_after_render:
    exit()
