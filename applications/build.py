#!/usr/bin/python3
import os

root_path = '/home/friederich/Documents/dev/neutrino/applications'
lib_list = ['dev_global', 'jupiter', 'polaris', 'venus', 'saturn']
for lib in lib_list:
    os.chdir(f"{root_path}/{lib}")
    build_cmd = f"python3 setup.py sdist"
    os.system(build_cmd)
    rm_dir_cmd = f"rm -r {lib}.egg-info"
    os.system(rm_dir_cmd)
    cp_cmd = f"cp -r dist/ {root_path}/"
    os.system(cp_cmd)
