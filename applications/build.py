#!/usr/bin/python3
import os


lib_list = ['dev_global', 'jupiter', 'polaris', 'venus', 'saturn']
for lib in lib_list:
    build_cmd = f"python3 {lib}/setup.py sdist"
    os.system(build_cmd)
    rm_dir_cmd = f"rm -r {lib}.egg-info"
    os.system(rm_dir_cmd)
