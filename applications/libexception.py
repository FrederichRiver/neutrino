#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


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
