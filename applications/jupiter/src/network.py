#! /usr/bin/python3
import json
from random import randint


class RandomHeader(object):
    def __init__(self):
        self.js = None
        with open('config/header.json', 'r') as f:
            result = f.read()
            self.js = json.loads(result)

    def __call__(self):
        index = randint(0, len(self.js)-1)
        header = {"User-Agent": self.js[str(index)]}
        return header


def delay(n):
    """
    Delay delta time not longer than n seconds.
    """
    import time
    time.sleep(randint(1, n))


def fetch_html_object(url, header):
    """
    result is a etree.HTML object
    """
    response = None
    while not response:
        response = requests.get(url, headers=header, timeout=3)
        delay(5)
    response.encoding = response.apparent_encoding
    result = etree.HTML(response.text)
    return result
