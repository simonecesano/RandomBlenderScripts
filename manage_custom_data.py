import bpy
import sys
import os
import argparse
import json
import re

# Replaces materials according to a JSON file
# provided as an option

# this parses args
def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []


parser = argparse.ArgumentParser(description='Replace/assign materials on blender file')

parser.add_argument('-e', '--edits_list',
                    metavar='json_file',
                    type=open
)

parser.add_argument('-p', '--palette_blend_file',
                    metavar='blender_file',
                    type=open
)

parser.add_argument('-c', '--clear', action='store_true')
parser.add_argument('-a', '--assign', action='store_true')

parser.add_argument('-M', '--list_materials',   action='store_true')
parser.add_argument('-P', '--list_parts',       action='store_true')
parser.add_argument('-A', '--list_assignments', action='store_true')

parser.add_argument('-f', '--output_format')

args = parser.parse_args(args=arg_after_dashes())


def strip_materials():
    for obj in bpy.data.objects:
        for i in range(len(obj.material_slots)):
            bpy.ops.object.material_slot_remove({'object': obj})

    for m in bpy.data.materials:
        bpy.data.materials.remove(m)    


edit_list = None

if (args.list_materials):
    list = []
    for mat in bpy.data.materials:
        
        mat['snazz'] = 12
        list.append([ mat.name, mat.users, mat.keys() ])
        for key in mat.keys():
            print(key, mat[key])
    # if args.format == 'json':
    print(json.dumps(list))
    #     pass
    # else:
    #     for mat in list:
    #         print(mat)
    # exit()
print(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)    
exit()
