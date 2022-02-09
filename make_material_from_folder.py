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
parser.add_argument('-o', '--output')

args = parser.parse_args(args=arg_after_dashes())

folder = os.path.abspath(args.material_folder if args.material_folder else '.')
folder_name = os.path.split(folder)[-1]


print(folder)

objs = [ob for ob in bpy.context.scene.objects if ob.type in ('MESH')]
bpy.ops.object.delete({"selected_objects": objs})    

bpy.ops.mesh.primitive_uv_sphere_add()
obj = bpy.context.active_object
obj.scale = (4.8, 4.8, 4.8)

mod = obj.modifiers.new(name='foobar', type="SUBSURF")
mod.subdivision_type = "CATMULL_CLARK"
mod.levels = 3
mod.render_levels = 5

obj = bpy.context.active_object

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

    print(folder_or_file_list)
    files = os.listdir(os.path.abspath(folder_or_file_list))
    files = [ os.path.abspath(os.path.join(folder_or_file_list, f)) for f in files ]

    material_files = {}


    for f in [ m for m in files if m.endswith('png') and p.findall(m) ]:
        t = p.findall(f)[0]
        material_files[t] = os.path.abspath(f)
    return material_files

def load_image(image_path, colorspace):
    path = os.path.abspath(image_path)
    img = bpy.data.images.load(path)
    img.colorspace_settings.name = "Raw"
    return img

def load_image_and_link(img, node_tree, links_list):
    def v_to_socket(socket, node, output):
        if isinstance(socket, bpy.types.NodeSocket):
            return socket
        elif isinstance(socket, str):
            n = node.outputs.get(socket) if output else node.inputs.get(socket)
            return n
        elif isinstance(socket, int):
            return node.outputs[socket] if output else node.inputs[socket]
        pass
    
    new_node = node_tree.nodes.new('ShaderNodeTexImage')

    new_node.image = img

    it = iter(links_list)
    for x in it:
        from_socket = v_to_socket(x, new_node, True)
        to_socket   = v_to_socket(next(it), new_node, False)
        link = node_tree.links.new(from_socket, to_socket)

material_images=classify_image(folder)

# print(material_images)
# exit()

mat = bpy.data.materials.new(name=folder_name)
mat.use_nodes = True

nodes = mat.node_tree.nodes
links = mat.node_tree.links

output  = nodes['Material Output']
bsdf    = nodes['Principled BSDF']

normal  = nodes.new('ShaderNodeNormalMap')
coords  = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeMapping')
value   = nodes.new('ShaderNodeValue')

disp_amount  = nodes.new('ShaderNodeValue')
displacement = nodes.new('ShaderNodeDisplacement')

value.outputs.get('Value').default_value = 2

mat.node_tree.links.new(value.outputs.get('Value'), mapping.inputs.get('Scale'))
mat.node_tree.links.new(coords.outputs.get('UV'),   mapping.inputs.get('Vector'))
mat.node_tree.links.new(disp_amount.outputs.get('Value'), displacement.inputs.get('Scale'))
mat.node_tree.links.new(displacement.outputs.get('Displacement'), output.inputs.get('Displacement'))


if material_images.get('METALLIC'):
    path = material_images.get('METALLIC')
    img = load_image(path, 'Non-Color')
    load_image_and_link(img, mat.node_tree, [ mapping.outputs.get('Vector'), 'Vector', 'Color', bsdf.inputs.get("Metallic") ])
    
if material_images.get('NORMAL'):
    path = material_images.get('NORMAL')
    img = load_image(path, 'Non-Color')
    load_image_and_link(img, mat.node_tree, [ mapping.outputs.get('Vector'), 'Vector', 'Color', normal.inputs.get("Color"), normal.outputs.get("Normal"), bsdf.inputs.get("Normal") ])

if material_images.get('OPACITY'):
    path = material_images.get('OPACITY')
    img = load_image(path, 'Non-Color')
    load_image_and_link(img, mat.node_tree, [ mapping.outputs.get('Vector'), 'Vector', 'Color', bsdf.inputs.get("Alpha") ])
    
if material_images.get('ROUGHNESS'):
    path = material_images['ROUGHNESS']
    img = load_image(path, 'Non-Color')
    load_image_and_link(img, mat.node_tree, [ mapping.outputs.get('Vector'), 'Vector', 'Color', bsdf.inputs.get("Roughness") ])

if material_images.get('BASECOLOR'):
    path = material_images['BASECOLOR']
    img = load_image(path, 'sRGB')
    load_image_and_link(img, mat.node_tree, [ mapping.outputs.get('Vector'), 'Vector', 'Color', bsdf.inputs.get("Base Color") ])

if material_images.get('HEIGHT'):
    path = material_images['HEIGHT']
    img = load_image(path, 'Raw')
    load_image_and_link(img, mat.node_tree, [ mapping.outputs.get('Vector'), 'Vector', 'Color', displacement.inputs.get("Height") ])

obj.data.materials.append(mat)

filepath = args.output if args.output else os.path.join(folder, folder_name + '.blend')

bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=filepath)
