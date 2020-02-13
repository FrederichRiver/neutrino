#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

DEST = '/opt/neutrino/'


def solve_dir(dir):
    """TODO: Install files compiled to dest directory.
    :direc: First iter directory
    :returns: None
    """
    # files = os.listdir(dir)
    files = [
        'neutrino.py', 'message.py', 'manage_tool.py',
        'config/conf.json', 'config/task.json',
        'config/Neutrino']
    for fi in files:
        obj_fi = dir + fi
        dest_fi = DEST + fi
        if os.path.isfile(obj_fi):
            print(obj_fi)
            cmd = "cp -u -v %s %s" % (obj_fi, dest_fi)
            os.system(cmd)
        elif os.path.isdir(fi):
            solve_dir(obj_fi+'/')
        else:
            pass


if __name__ == "__main__":
    solve_dir('./')
