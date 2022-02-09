import bpy
import sys
import os
import argparse

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []

parser = argparse.ArgumentParser(description='Import/export GLTf')

parser.add_argument('input', metavar='gltf/blender file', type=str, help='a file to import or export')
parser.add_argument('-o', '--output')
args = parser.parse_args(args=arg_after_dashes())

if args.input.endswith('glb'):
    for obj in bpy.context.scene.objects: 
        bpy.data.objects.remove(obj, do_unlink=True)
    
    bpy.ops.import_scene.gltf(filepath=args.input)
    output = args.output if args.output else args.input.replace('.glb', '.blend')
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(output))
    exit()


if args.input.endswith('blend'):
    bpy.ops.wm.open_mainfile(filepath=args.input)
    
    output = args.output if args.output else args.input.replace('.blend', '.glb')
    print(os.path.abspath(output))
    bpy.ops.export_scene.gltf(filepath=os.path.abspath(output), export_format='GLB', export_materials='EXPORT')
    exit()
