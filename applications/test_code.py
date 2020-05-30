input_list = [i for i in range(10)]
input_list = None
class test(object):
    def __init__(self, x):
        pass

    def __enter__(self):
        print('>enter')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # print(exc_type, exc_val, exc_tb)
        if not exc_type:
            raise exc_val

with test(input_list):
    for x in input_list:
        print(x)
