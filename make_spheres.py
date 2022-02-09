import bpy
import sys
import os
import argparse
import mathutils

def arg_after_dashes():
    try:
        idx = sys.argv.index("--")
        return sys.argv[idx+1:] # the list after '--'
    except ValueError as e: # '--' not in the list:
        return []

parser = argparse.ArgumentParser(description='Make palette file')

parser.add_argument('-q', '--quantity')
parser.add_argument('-o', '--output')

bpy.ops.mesh.primitive_uv_sphere_add()
bpy.ops.object.shade_smooth()

obj = bpy.context.active_object

obj.scale = (4.8, 4.8, 4.8)

print(obj)

for x in range(0, 12):
    for y in range(0, 12):
        d = obj.copy()
        (dx,dy,dz) = (12.0 * x, 12.0 * y, 0.0)
        d.location = d.location + mathutils.Vector((dx,dy,dz))
        bpy.context.collection.objects.link(d)
        
bpy.ops.wm.save_as_mainfile(filepath='./balls.blend')

