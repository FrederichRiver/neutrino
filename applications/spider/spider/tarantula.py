#!/usr/bin/python3
import requests


class tarantula(object):
    def __init__(self):
        self.start_url = 'https://www.zhihu.com/signin?next=%2F'
        # self.start_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.session = requests.session()
        self.headers = {
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }

    def run(self):
        import re
        import json
        response = self.session.get(self.start_url, headers=self.headers)
        result = response.headers
        pattern = r'_xsrf=([a-z0-9\-]+)'
        xsrf = re.findall(pattern, str(response.headers))
        print(xsrf[0])
        with open('zhihu.header', 'w') as f:
            f.write(str(response.headers))
        with open('zhihu.text', 'w') as f:
            f.write(str(response.text))
        form_data = {
            "name": ''
        }
        p2 = r'"captchaNeeded":([a-z]+)'
        cap_need = re.findall(p2, response.text)
        print(cap_need[0])
        #self.captcha_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"
        #cap_result = self.session.post(self.captcha_url, headers=self.headers)
        #print(cap_result)
        # self.login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
        # result = self.session.post(self.login_url)
        # print(result)


def _get_signature(self, timestamp):
    ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
    grant_type = self.login_data['grant_type']
    client_id = self.login_data['client_id']
    source = self.login_data['source']
    ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
    return ha.hexdigest()


def _get_xsrf():
    pass

"""
request_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
# "cookie": '_zap=9d5d1617-95e1-41b0-8fdc-9ebe08f532c7; d_c0="ANDXmq7i7xCPTlIkz1GioQD14MrkA-BdxWU=|1583756348"; _ga=GA1.2.750210372.1583756361; tst=r; _xsrf=lnmXFSI9tM6XUerDd72s7hBBVYaqGSUJ; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1583756360,1584202172,1584854816; _gid=GA1.2.320287222.1584854817; q_c1=de90185a939644b3aaf4b4c396b285ad|1584875523000|1584875523000; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1584877986; capsion_ticket="2|1:0|10:1584878087|14:capsion_ticket|44:YjQzYjkzZDA3NDVlNDhhMWI5YzFkYjE1NDEyYjQyNjk=|aa08a44c5c450f7b8f3402df4fdd25ad69d88701c00ddf06d4c719cde48d6eb4"; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1584878205|158487548',
headers = {
    "x-xsrftoken": 'lnmXFSI9tM6XUerDd72s7hBBVYaqGSUJ',
    "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    "content-type": 'application/x-www-form-urlencoded'
    "x-zse-83": '3_2.0'
}
form_data = None
timestamp = str(int(time.time()*1000))

resp = self.session.get(api, headers=headers)
show_captcha = re.search(r'true', resp.text)
if show_captcha:
    put_resp = self.session.put(api, headers=headers)
    img_base64 = re.findall(
        r'"img_base64":"(.+)"', put_resp.text, re.S)[0].replace(r'\n', '')
    with open('./captcha.jpg', 'wb') as f:
        f.write(base64.b64decode(img_base64))
        img = Image.open('./captcha.jpg')
"""


if __name__ == "__main__":
    event = tarantula()
    event.run()
