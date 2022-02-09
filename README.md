# Blender scripts

This is a bunch of scripts that try to create, convert or massage 3D assets with Blender.

The goal is for all of them to _at least_

- take zero, one or more files as input
- generate an output file

So that they can form a modular transformation toolchain.

They should all run like this:

    blender -b some_file.blend --python some_script.py -- --an_option --output some_other_file.blend

or 

    blender -b --python some_script.py -- --json some_data.json --output some_other_file.blend

### Notes

This repo conforms to Sturgeon's law.

## details

### blender_arg_parse.py

Template for passing command line arguments to a blender-python script  

### describe_material.py

Utility to dump a textual description of materials in a .blend file

### import_fbx.py

Imports an FBX file and saves it as Blender

### import_gltf.py

Imports a GLTF file and saves it as Blender

### import_obj.py

Imports an OBJ file and saves it as Blender

### make_material_from_folder.py

Takes a folder of appropriately named image files and creates a Blender material 

### make_palette.py

Takes a bunch of material files created with make_material_from_folder.py and collates them into one file

### make_spere_with_catmull_clark.py

Makes a sphere using Catmull-Clark subdiv (useful to see how to apply a modifier)

### make_spheres.py

Makes a number of spheres on a grid

### manage_custom_data.py

Test for updating custom data on a Blender file

### material_classifier.py

Test for classifying materials files according to the name; code used later in make_material_from_folder.py

### parse_gltf.py

Stub of an attempt at parsing GLTF directly

### render_to_image.py

Render a blend file to a PNG 

### render_to_image_gpu.py

Render a .blend file to PNG using the GPU

### replace_materials.py

Replaces materials in a file with materials with the same name from another file; attempt at upgrading materials via script before rendering

### squeeze_texture.py

Takes a material file and reduces its size by converting images to jpegs and scaling them down

### unwrap_mesh.py

Attempts at unwrapping meshes - not working

