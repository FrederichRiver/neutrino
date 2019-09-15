#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


class NoFileException(BaseException):
    def __init__(self, file_name):
        """TODO: Docstring for __init__.

        :file_name: TODO
        :returns: TODO

        """
        super(BaseException, self).__init__()
        self.file_name = file_name

    def __str__(self):
        return f"{time.ctime()}: {self.file_name} could not be found.\n"


if __name__ == "__main__":
    import os, sys
    with open('temptest', 'a') as f:
        os.dup2(f.fileno(), 1)
        os.dup2(f.fileno(), 2)
    try:
        if True:
            raise NoFileException('Test')
    except:
        sys.stdout.flush() 
        sys.stderr.flush()
        #sys.stdout.write(NoFileException('Test1'))
