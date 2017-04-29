'''
Created on Apr 23, 2017

@author: frederich
'''
import hashlib
def encrypt(content):
    if isinstance(content, str)==True:
        m=hashlib.md5()
        m.update(content)
        return m.hexdigest()
    else:
        return None
def decrypt(content):
    pass