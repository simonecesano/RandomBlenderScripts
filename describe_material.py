import bpy
import sys
import os
import argparse
import json
import re
import time

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []


parser = argparse.ArgumentParser(description='Replace/assign materials on blender file')

parser.add_argument('-f', '--material_folder')

args = parser.parse_args(args=arg_after_dashes())

# print(args.material_folder)
# print([m for m in os.listdir(args.material_folder) if m.endswith('png') ])

file_types = [
    "BASECOLOR",
    "NORMAL",
    "ROUGHNESS",
    "METALLIC",
    "HEIGHT",
    "OPACITY",
    "AMBIENTOCCLUSION"
]
def classify_image(file):
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
    try:
        t = p.findall(file)[0]
        return t.upper()
    except:
        return 'NONE'

# a new material node tree already has a diffuse and material output node

def print_indent(level, *a):
    if level:
        print(" " * (level), *a)
    else:
        print(*a)

def recurse_node_tree(node_tree):
    nodes = node_tree.nodes
    for n in nodes:
        print_indent(2, 'NODE:', n.name, n.type)
        # print(dir(n));
        if n.type == "TEX_IMAGE":
            print_indent(4, 'IMG', n.image.name, " | ", n.image.colorspace_settings.name, " | ", classify_image(n.image.filepath), " | ", os.path.basename(n.image.filepath))
        for o in n.inputs:
            if o.is_linked:
                print_indent(4, 'INPUT:', o.name)
                for l in o.links:
                    print_indent(6, o.name, ' <= ', l.from_node.name, "|",  l.from_socket.name)
        for o in n.outputs:
            if o.is_linked:
                print_indent(4, 'OUTPUT:', o.name)
                for l in o.links:
                    print_indent(6, o.name, ' => ', l.to_node.name, "|",  l.to_socket.name)
        if n.type == "GROUP":
            recurse_node_tree(n.node_tree)
    pass
        
for mat in bpy.data.materials:
    if mat.node_tree:
        print_indent(0, 'MATERIAL:', mat.name)
        nodes = mat.node_tree.nodes
        for n in nodes:
            print_indent(2, 'NODE:', n.name, n.type)
            # print(dir(n));
            if n.type == "TEX_IMAGE":
                # print(n.image.colorspace_settings)
                print_indent(4, 'IMG', n.image.name, " | ", n.image.colorspace_settings.name, " | ", classify_image(n.image.filepath), " | ", os.path.basename(n.image.filepath))
            if n.type == "GROUP":
                # print_indent(4, 'IMG', n.image.name, " | ", n.image.colorspace_settings.name, " | ", classify_image(n.image.filepath), " | ", os.path.basename(n.image.filepath))
                recurse_node_tree(n.node_tree)
            for o in n.inputs:
                if o.is_linked:
                    print_indent(4, 'INPUT:', o.name)
                    for l in o.links:
                        print_indent(6, o.name, ' <= ', l.from_node.name, "|",  l.from_socket.name)
            for o in n.outputs:
                if o.is_linked:
                    print_indent(4, 'OUTPUT:', o.name)
                    for l in o.links:
                        print_indent(6, o.name, ' => ', l.to_node.name, "|",  l.to_socket.name)
exit()











output  = nodes['Material Output']
bsdf    = nodes['Principled BSDF']

normal  = nodes.new('ShaderNodeNormalMap')
coords  = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeMapping')
value   = nodes.new('ShaderNodeValue')

for input in bsdf.inputs:
    print(input.name)

print('-' * 80)


n = mat.node_tree.nodes.new('ShaderNodeTexImage')
print(n)
for output in n.outputs:
    print(output.name)

print('-' * 80)
# exit()

print('output', n.outputs[0])
print(isinstance(n.outputs[0],  bpy.types.NodeSocketColor))

print('output', n.outputs[0].name)
print('output', getattr(n, 'outputs')[0].name)
print('output', n.outputs.get("Color").name)

print('input', bsdf.inputs[0].name)
print('input', bsdf.inputs.get("Base Color").name)

# exit()

