

from gltflib import GLTF

gltf = GLTF.load('foo.glb')

for b in gltf.model.buffers:
    print(b)
