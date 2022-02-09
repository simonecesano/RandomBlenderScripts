import bpy
import sys
import os

bpy.ops.mesh.primitive_uv_sphere_add()
obj = bpy.context.active_object
obj.scale = (4.8, 4.8, 4.8)
mod = obj.modifiers.new(name='foobar', type="SUBSURF")
mod.subdivision_type = "CATMULL_CLARK"
mod.levels = 3
mod.render_levels = 5
