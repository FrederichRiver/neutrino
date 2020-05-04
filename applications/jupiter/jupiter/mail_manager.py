#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header


__version__ = '2.0.2'


class MailServer(object):
    """
    A robot who send mails in templates.
    version 2.0
    """
    def __init__(self):
        """
        Init basic infomation of mail sender.
        """
        from jupiter.utils import read_url, CONF_FILE
        self.__mail_host = "smtp.163.com"
        self.__mail_user = "friederich"
        self.__mail_pw = "monster1983"
        self.sender = "Friederich River<friederich@163.com>"
        self.mail_template_path = read_url('path_template', CONF_FILE)
        self.mail_server = smtplib.SMTP()

    def smtp_config(self):
        try:
            self.mail_server = smtplib.SMTP()
            self.mail_server.connect(self.__mail_host, 25)
            self.mail_server.login(self.__mail_user, self.__mail_pw)
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    def smtp_ssl_config(self):
        try:
            self.mail_server = smtplib.SMTP_SSL(self.__mail_host,465)
            self.mail_server.login(self.__mail_user, self.__mail_pw)
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    def send_mail(self, sender, message):
        """
        Agent for sending mails.
        """
        try:
            self.mail_server.sendmail(sender, message['To'].split(','), message.as_string())
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    def auto_load_mail(self):
        import json
        mail_list = json.loads(open("/home/friederich/Documents/dev/neutrino/applications/config/mail_config.json").read())
        for mail_param in mail_list:
            mail = self.mail_resolve(mail_param)
            self.send_mail(self.sender, mail())
            
    def mail_resolve(self, mail):
        mail_obj = guest_mail(mail['Type'])
        mail_obj.set_mail(
                        title=mail['Title'], content=mail['Content'],
                        mail_list=mail['Reciever']
                    )
        if 'Attachment' in mail.keys():
            for att in mail['Attachment']:
                a = MailAttachmentBase(att['url'])
                a.set_attach(att['alias'])
                mail_obj.add_attach(a())
        return mail_obj

class MailContentBase(object):
    def __init__(self, MAIL_TYPE):
        import datetime
        from email.mime.multipart import MIMEMultipart
        self.mail_content = MIMEMultipart()
        self.mail_type = MAIL_TYPE
        self.template_path = '/home/friederich/Documents/dev/neutrino/applications/template/'   

    def set_mail(self, **args):
        for k in args.keys():
            if k == 'mail_list':
                self._set_send_to(args.get('mail_list')) 
            elif k == 'title':
                self._set_subject(args.get('title'))
            elif k == 'content': 
                self._set_content(args.get('content')) 

    def _set_send_to(self, mail_list):
        raise MailDefException("_set_send_to")

    def _set_subject(self, subject):
        raise MailDefException("_set_subject")

    def _set_content(self, content_url):
        raise MailDefException("_set_content")

    def add_attach(self, attach_list):
        if isinstance(attach_list, MIMEText):
            self.mail_content.attach(attach_list)
        elif isinstance(attach_list, list):
            for att in attach_list:
                self.mail_content.attach(att)
        else:
            self.mail_content.attach(attach_list)
    
    def __call__(self):
        return self.mail_content

class MailAttachmentBase(object):
    def __init__(self, url):
        self. __attachment = MIMEText( open(url, 'rb').read(), 'base64', 'utf-8')

    def set_attach(self, attach_file):
        self. __attachment["Content-Type"] = auto_content_type(attach_file)
        self. __attachment.add_header('Content-Disposition','attachment',filename = attach_file)

    def __call__(self):
        return self.__attachment


class guest_mail(MailContentBase):
    """
    Guest mail is base on MailContentBase.
    """
    def _set_send_to(self, mail_list):
        self.mail_content['To'] = ','.join(mail_list)

    def _set_subject(self, title):
        self.mail_content['Subject'] = Header(title, 'utf-8')

    def _set_content(self, content_url):
        mail_template = self.template_path + content_url
        content = open(mail_template, 'r').read()
        self.mail_content.attach(MIMEText(content, self.mail_type, 'utf-8'))


class MailDefException(Exception):
    def __str__(self, func_name):
        return f"{func_name} has not been defined."
"""
text/plain（纯文本）
text/html（HTML文档）
application/xhtml+xml（XHTML文档）
image/gif（GIF图像）
image/jpeg（JPEG图像）【PHP中为：image/pjpeg】
image/png（PNG图像）【PHP中为：image/x-png】
video/mpeg（MPEG动画）
application/octet-stream（任意的二进制数据）
application/pdf（PDF文档）
application/msword（Microsoft Word文件）
message/rfc822（RFC 822形式）
multipart/alternative（HTML邮件的HTML形式和纯文本形式，相同内容使用不同形式表示）
application/x-www-form-urlencoded（使用HTTP的POST方法提交的表单）
multipart/form-data（同上，但主要用于表单提交时伴随文件上传的场合）
"""       


def auto_content_type(filename):
    ext_name = filename.split('.')[-1]
    ext_name = ext_name.lower()
    if ext_name == 'txt':
        return 'text/plain'
    elif ext_name == 'html':
        return 'text/html'
    elif ext_name == 'gif':
        return 'image/gif'
    elif ext_name == 'jpg' or ext_name == 'jpeg':
        return 'image/jpeg'
    elif ext_name == 'png':
        return 'image/png'
    elif ext_name == 'mpeg':
        return 'video/mpeg'
    elif ext_name == 'xls' or ext_name == 'xlsx':
        return 'application/octet-stream'
    elif ext_name == 'pdf':
        return 'application/pdf'
    elif ext_name == 'doc' or ext_name == 'docx':
        return 'application/msword'
    else:
        return 'text/plain'    


def test():
    from datetime import date
    l = ['Fred<hezhiyuan_tju@163.com>','Guest<362381761@qq.com>']
    t = "This is a test."
    att_path = '/home/friederich/Documents/dev/neutrino/applications/dist/data.xls'
    Mercury = MailServer()
    Mercury.smtp_ssl_config()
    mail_content = guest_mail('plain')
    mail_content.set_mail(mail_list = l, title = f"Close Price {date.today()}", content = "This is a test.")
    att1 = MailAttachmentBase(att_path)
    att1.set_attach('data.xls')
    mail_content.add_attach(att1())
    result = mail_content.get_mail_content()
    Mercury.send_mail(Mercury.sender, result)

if __name__ == "__main__":
    filename = 'test-doc-pdf'
    filename = filename.upper()
    Mercury = MailServer()
    Mercury.smtp_ssl_config()
    mail_content = guest_mail('plain')
    Mercury.auto_load_mail()