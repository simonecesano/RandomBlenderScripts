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

def enable_gpus(device_type, use_cpus=False):
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cuda_devices, opencl_devices = cycles_preferences.get_devices()

    if device_type == "CUDA":
        devices = cuda_devices
    elif device_type == "OPENCL":
        devices = opencl_devices
    else:
        raise RuntimeError("Unsupported device type")

    activated_gpus = []

    for device in devices:
        if device.type == "CPU":
            device.use = use_cpus
        else:
            device.use = True
            activated_gpus.append(device.name)

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"

    return activated_gpus


enable_gpus("CUDA")
bpy.context.scene.cycles.device = 'GPU'
print(bpy.context.scene.cycles.device)

parser = argparse.ArgumentParser(description='Render Blender file')

parser.add_argument('-c', '--clear', action='store_true')
parser.add_argument('-a', '--assign', action='store_true')

parser.add_argument('-r', '--resolution_percentage')

parser.add_argument('-f', '--output_format')
parser.add_argument('-q', '--exit_after_render')

args = parser.parse_args(args=arg_after_dashes())

bpy.context.scene.render.filepath = bpy.data.filepath.replace('.blend', '.png')


bpy.context.scene.render.resolution_percentage = int(args.resolution_percentage) if args.resolution_percentage else 100 

bpy.context.scene.render.engine = "CYCLES"

bpy.ops.render.render(write_still = True)

if args.exit_after_render:
    exit()
