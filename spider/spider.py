#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
}
content =requests.get("http://www.zhihu.com", headers=headers)

html = etree.HTML(content.text)
xsrf = html.xpath("//input")
for x in xsrf:
    print(x)

