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

parser.add_argument('-p', '--palette_blend_file')

parser.add_argument('-c', '--clear', action='store_true')
parser.add_argument('-a', '--assign', action='store_true')

parser.add_argument('-M', '--list_materials',   action='store_true')
parser.add_argument('-P', '--list_parts',       action='store_true')
parser.add_argument('-A', '--list_assignments', action='store_true')

parser.add_argument('-f', '--output_format')
parser.add_argument('-o', '--output_file')
parser.add_argument('-q', '--quit_when_done', action='store_true')

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
        list.append(mat.name)
    if args.format == 'json':
        print(json.dumps(list))
        pass
    else:
        for mat in list:
            print(mat)
    exit()

if (args.list_parts):
    list = []
    for obj in bpy.data.objects:
        list.append(obj.name)
    if args.format == 'json':
        print(json.dumps(list))
        pass
    else:
        for mat in list:
            print(mat)
    exit()

if (args.list_assignments):
    list = []
    for obj in [ o for o in bpy.data.objects if o.type == "MESH" ]:
        list.append({ "part": obj.name, "materials": [m.material.name for m in obj.material_slots] })
    print(json.dumps(list))
    exit()
    
if args.edits_list:
    palette_path=args.palette_blend_file

    if os.path.isfile(palette_path):
        try:
            with bpy.data.libraries.load(os.path.abspath(palette_path), link=False) as (data_from, data_to):
                data_to.materials = data_from.materials    
        except BaseException as err:
            sys.stderr.write("ERROR: palette file not loaded\n")
            sys.stderr.write(str(err) + "\n")
            exit()
    else:
        sys.stderr.write("ERROR: palette file not found\n")
        exit()
        
    edit_list = json.load(args.edits_list)
    args.edits_list.close()

    output_file = args.output_file

    if not len(output_file):
        basename = os.path.basename(args.edits_list.name)
        md5 = re.compile('[a-z0-9]{32,32}').findall(basename)[0];
        output_file=bpy.data.filepath.replace('.blend', '-' + md5 + '.blend');

    for e in edit_list:
        part = bpy.data.objects[e['part']]
        mat  = bpy.data.materials[e['material']]
        part.data.materials[0] = mat
    try:
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=output_file)    
    except BaseException as err:
        sys.stderr.write("ERROR: could not save file\n")
        sys.stderr.write(str(err) + "\n")
        exit()

        
if args.quit_when_done:
    exit()
