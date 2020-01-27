#!/usr/bin/python3

import os
import re
import tarfile

DEST = "/opt/neutrino/"

SRC = "applications/"

file_list = ["neutrino.py", "install.py"]


def package(file_list):
    for code_file in file_list:
        object_file = SRC + code_file
        dest_file = "dist/src/" + code_file
        cmd = f"cp -u -v {object_file} {dest_file}"
        # print(cmd)
        os.system(cmd)


def solve_version():
    version = None
    with open('dist/src/VERSION', 'r') as f:
        version = f.read()
        # print(version)
    result = re.match(r'(\d.\d).(\d+)', version)
    version = result.group(1) + '.' + str(int(result.group(2))+1)
    with open('dist/src/VERSION', 'w') as f:
        f.write(version)
    return version


def make_tar(output_filename, source_dir):
    try:
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'pack':
        package(file_list)
    elif sys.argv[1] == 'tar':
        v = solve_version()
        make_tar(f"dist/neutrino-{v}.tar.gz", "dist/src")
    elif sys.argv[1] == 'v':
        solve_version()
