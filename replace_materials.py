import bpy
import sys
import os
import argparse
import json
import re
import hashlib
from pathlib import Path

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

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

edit_list = None


if (args.list_materials):
    list = []
    for mat in bpy.data.materials:
        list.append(mat.name)
    if args.output_format == 'json':
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
    if args.output_format == 'json':
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

def process_edits_list(edits_list):
    # for (i, m) in enumerate(edit_list):
    #     print(m)
    #     if isinstance(m, list):
    #         print('list')
    #         edit_list[i] = { "part": m[0], "file": m[1], "material": m[2] }
    for (i, m) in enumerate(edit_list):
        if isinstance(m, dict):
            edit_list[i] = [m["part"], m.get("file"), m["material"] ]

    for (i, m) in enumerate(edit_list):
        if not m[1]:
            for path in Path('/home/simone/lp_wf_demo/materials').rglob(m[2]):
                m[1] = str(path.resolve())
            
    for (i, m) in enumerate(edit_list):
        m[2] = m[2].replace('.blend', "")
        
    return [ e for e in edit_list if e[0] ]

if args.edits_list:
    edit_list = json.load(args.edits_list)

    # print(edit_list)

    edit_list = process_edits_list(edit_list)

    # print(edit_list)
    
    # exit()

    # print(set([m[1] for m in edit_list]))

    edits_by_file = {}
    
    for m in edit_list:
        if not m[1] in edits_by_file.keys(): edits_by_file[m[1]] = []
        edits_by_file[m[1]].append(m[2])

    for k in edits_by_file.keys():
        edits_by_file[k] = list(set(edits_by_file[k]))
        
    print(edits_by_file)
    
    # exit()

    for mat_file in edits_by_file.keys():
        if os.path.isfile(mat_file):
            print(mat_file)
            try:
                with bpy.data.libraries.load(os.path.abspath(mat_file), link=False) as (data_from, data_to):
                    # print([m for m in data_from.materials if m in mat_file])
                    # print([m for m in data_from.materials if m in edits_by_file[mat_file]])
                    # this is kinda dirty but it works if one sticks to the rule 
                    # (1) one file, one material (2) material name contained in file name
                    data_to.materials = [m for m in data_from.materials if m in mat_file]    
                    print(data_to.materials)
                    for (i, m) in enumerate(edit_list):
                        if m[1] == mat_file:
                            print(m, mat_file)
                            edit_list[i][2] = data_to.materials[0]

                    
            except BaseException as err:
                sys.stderr.write("ERROR: palette file not loaded\n")
                sys.stderr.write(str(err) + "\n")
                exit()
        else:
            sys.stderr.write("ERROR: palette file not found\n")
            exit()

    for e in edit_list:
        print([o.name for o in bpy.data.objects if o.name in e[0] ])

        # gotta throw something here if no part name is found
        part_name = [o.name for o in bpy.data.objects if o.name in e[0] ][0]
        part = bpy.data.objects[part_name]
        mat  = bpy.data.materials[e[2]]

        print("Assigning material {1} to part {0}".format(part.name, mat.name))

        if part.data.materials:
            part.data.materials[0] = mat
        else:
            part.data.materials.append(mat)
        
    output_file = args.output_file

    print(args.edits_list.name)
    if not output_file:
        basename = os.path.basename(args.edits_list.name)
        md5 = md5(args.edits_list.name)
        output_file=bpy.data.filepath.replace('.blend', '-' + md5 + '.blend');

    print("Saving file %s" % os.path.abspath(output_file))
    args.edits_list.close()
        
    try:
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=output_file)    
    except BaseException as err:
        sys.stderr.write("ERROR: could not save file\n")
        sys.stderr.write(str(err) + "\n")
        exit()

        
if args.quit_when_done:
    exit()
