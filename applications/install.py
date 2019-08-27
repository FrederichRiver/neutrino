#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

dest = '/opt/neutrino/'


def _solve_dir(direc, path=''):
    """TODO: Install files compiled to dest directory.
    :direc: First iter directory
    :returns: None
    """
    if os.path.exists(dest + path) is False:
        os.system('mkdir {}'.format(dest + path))
    files = os.listdir(direc)
    for fi in files:
        obj_fi = direc + fi
        dest_fi = dest + path + fi.replace('.cpython-36', '')
        if os.path.isfile(obj_fi):
            cmd = "cp -u -v %s %s" % (obj_fi, dest_fi)
            os.system(cmd)
        elif os.path.isdir(fi):
            input_path = path + fi + '/'
            _solve_dir(obj_fi+'/', input_path)
        else:
            pass


if __name__ == "__main__":
    _solve_dir('__pycache__/')
