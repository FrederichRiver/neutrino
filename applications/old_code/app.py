#!/usr/bin/python3
"""
Created by Frederich River, 22 Apr, 2018

"""
#create a selector
class selector(object):
    def __init__(self):
        self.obj = []
        self.obj2 = {}
    def read(self, content):
        self.obj = content
    def result(self, nu=3):
        return self.obj[:nu]
    def result2(self, nu=3):
        return self.obj2
class randomselector(selector):
    pass
class orderingselector(selector):
    pass
#a small judger
#ultility functions
class ultility(object):
    def __init__(self, x):
        self.input = x
    def fun(self,x):
        y =2*x
        return y
    def ultility(self):
        self.result = self.fun(self.input)
        return self.result


#sorting
#output result
if __name__ == '__main__':
    a = selector()
    a.read(['a','b','c','d','e','f'])
    print(a.result())
    
    exam = ultility([2,3,4])
    print(exam.ultility())
