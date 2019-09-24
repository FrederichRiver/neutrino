#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time


DM_MSG = "neutrino start|stop|help"
DM_START = "{t}: Neutrino id is {pid}.\n"
DM_ALIVE = "{0}: Neutrino is running.\n"
DM_STOP = "{0}: Neutrino is stopped.\n"
DM_NOT_RUN = "Neutrino is not running.\n"
DM_CHECK_TASK = "{}: Checking task file.\n"
DM_MISS_TASK = "{}: Task plan file is not found.\n"


class NoFileException(BaseException):
    def __init__(self, file_name):
        super(BaseException, self).__init__()
        self.file_name = file_name

    def __str__(self):
        return f"{time.ctime()}: {self.file_name} could not be found.\n"


class AccountException(BaseException):
    def __str__(self):
        return "[Error 1]: Account error."


class TypeException(BaseException):
    def __str__(self):
        return "[Error 2]: Type error."


if __name__ == "__main__":
    pass
