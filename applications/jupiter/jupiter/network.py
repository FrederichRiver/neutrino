#! /usr/bin/python3
import json
from random import randint


class cookie(object):
    def __init__(self):
        from dev_global.env import COOKIE_FILE
        self.js = None
        with open(COOKIE_FILE, 'r') as f:
            result = f.read()
            self.js = json.loads(result)

    def get_cookie(self, name: str) -> str:
        return self.js[name]


class RandomHeader(object):
    def __init__(self):
        from dev_global.env import HEAD_FILE
        self.js = None
        with open(HEAD_FILE, 'r') as f:
            result = f.read()
            self.js = json.loads(result)
        self.header = None

    def set_user_agent(self):
        index = randint(0, len(self.js)-1)
        self.header = {"User-Agent": self.js[str(index)]}

    def set_refer(self, reference):
        if not self.header:
            self.set_user_agent()
        self.header['Referer'] = reference

    def __call__(self):
        index = randint(0, len(self.js)-1)
        header = {"User-Agent": self.js[str(index)]}
        return header


class userAgent(object):
    """
    Example:
    object = usrAgent()
    result = object(), get a str type result which is User_Agent.
    result = object.random_agent, get a random User_Agent from liboratory.
    """
    def __init__(self):
        from dev_global.env import HEAD_FILE
        self.js = None
        with open(HEAD_FILE, 'r') as f:
            result = f.read()
            self.js = json.loads(result)
        self.header = None

    def random_agent(self) -> str:
        i = randint(0, len(self.js)-1)
        return self.js[str(i)]

    def __call__(self):
        return self.js["10"]


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


if __name__ == "__main__":
    cuky = cookie()
    result = cuky.get_cookie('cninfo')
    print(result)
