#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

DEST = '/opt/neutrino/'

SERVER = os.getenv('SERVER')
if not SERVER:
    DEST2 = '/home/friederich/Documents/dev/neutrino/applications/package/'


def solve_dir(dir):
    """TODO: Install files compiled to dest directory.
    :direc: First iter directory
    :returns: None
    """
    # files = os.listdir(dir)
    files = [
        'neutrino.py',
        'manage_tool.py',
        'config/conf.json',
        'config/Neutrino',
        'config/task.json',
        'config/cookie.json',
        'config/new-energy-tag.json',
        'config/semi-conductor-tag.json'
        ]
    for fi in files:
        obj_fi = dir + fi
        dest_fi = DEST + fi
        
        if os.path.isfile(obj_fi):
            print(obj_fi)
            cmd = "cp -u -v %s %s" % (obj_fi, dest_fi)
            os.system(cmd)
            if not SERVER:
                dest_fi2 = DEST2 + fi
                cmd = "cp -u -v %s %s" % (obj_fi, dest_fi2)
                os.system(cmd)
        elif os.path.isdir(fi):
            solve_dir(obj_fi+'/')


if __name__ == "__main__":
    solve_dir('./')
