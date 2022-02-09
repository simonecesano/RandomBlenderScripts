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


parser = argparse.ArgumentParser(description='Replace/assign materials on blender file')

parser.add_argument('-f', '--material_folder')

args = parser.parse_args(args=arg_after_dashes())

print(args.material_folder)
# print([m for m in os.listdir(args.material_folder) if m.endswith('png') ])

def classify_image(folder_or_file_list):
    file_types = [
        "BASECOLOR",
        "NORMAL",
        "ROUGHNESS",
        "METALLIC",
        "HEIGHT",
        "OPACITY",
        "AMBIENTOCCLUSION"
    ]
    
    p = re.compile("(" + "|".join(file_types) + ")", re.IGNORECASE)

    files = os.listdir(folder_or_file_list)
    # _material_files = [ m for m in files if m.endswith('png') and p.findall(m) ]
    material_files = {}
    
    for f in [ m for m in files if m.endswith('png') and p.findall(m) ]:
        t = p.findall(f)[0]
        material_files[t] = f
    return material_files

print(classify_image(args.material_folder))
               
exit()

for m in bpy.data.materials:
    if m.node_tree:
        # print(m)    
        for n in m.node_tree.nodes:
            print(n)
            print(n.name, n.type)
            if n.type=='TEX_IMAGE':
                print(n.image)

        print('----------------------------------------')

        for l in m.node_tree.links:
            print('from', l.from_node.type, l.from_socket.name, l.from_socket.label)
            print('to', l.to_node.type, l.to_socket.name, l.to_socket.label)

            print("::".join([ l.from_node.type, l.from_socket.name, l.to_node.type, l.to_socket.name ]))
            print('----------------------------------------')
exit()
