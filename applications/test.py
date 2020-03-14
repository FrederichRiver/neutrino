#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test():
    import test2
    import imp
    import time
    mod = []
    d = {}
    mod.append(test2)
    while 1:
        for m in mod:
            imp.reload(m)
            for f in m.__all__:
                d[f] = eval(f"{m.__name__}.{f}")
        print(d)
        for k, v in d.items():
            v()
        time.sleep(10)


if __name__ == "__main__":
    test()
