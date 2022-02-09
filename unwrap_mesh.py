import bpy
import bmesh
from mathutils import Vector

print( "------------" )

shape_key_name = "test"
object_name = "420_Vamp"
uv_map_name = "UVMap"

obj = bpy.data.objects[object_name]

# Prepare the shape keys

if not obj.data.shape_keys:
    obj.shape_key_add( name = "Basis" )

shape_key = obj.data.shape_keys.key_blocks.get( shape_key_name )

if shape_key:
    obj.shape_key_remove( shape_key )

shape_key = obj.shape_key_add( name = shape_key_name )

# Cut the mesh

# Get a bmesh from the object mesh
bm = bmesh.new()
bm.from_mesh( obj.data )

# Prepare the mesh
bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

# Split edges that have seam and link to 2 faces
edges = [e for e in bm.edges if e.seam and len(e.link_faces) == 2]

print(len(edges))
bmesh.ops.split_edges( bm, edges = edges )

# Give the new geometry back to the object
# bmesh.update_edit_mesh(obj.data, False, False)

bm.to_mesh( obj.data )

# Get the uv map
uv_map = obj.data.uv_layers[uv_map_name]

# Assign the coordinates to the shape key
print(uv_map)


print(len(obj.data.loops))
print(len(uv_map.data))


for v in obj.data.vertices:
    v.co = Vector( (1, 0, 2) )


# exit()
for loop, uv_data in zip( obj.data.loops, uv_map.data ):
    uv = uv_data.uv
    # print(loop)
    # print(uv_data)
    vertex_index = loop.vertex_index
    edge_index = loop.edge_index
    # print(vertex_index, edge_index)
    # print(obj.data.vertices[vertex_index].co)

    # obj.data.vertices[vertex_index].co = Vector( (uv.x, 0, uv.y) )
    bm.verts[vertex_index].co = Vector( (uv.x, uv.y, 0) )
    # shape_key.data[vertex_index].co = Vector( (uv.x, 0, uv.y) )

bm.to_mesh( obj.data )

# bmesh.update_edit_mesh(obj.data, False, False)
# obj.data.update()    

bpy.ops.wm.save_as_mainfile(filepath='flattened.blend')
