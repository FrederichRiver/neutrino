#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header


__version__ = '1.0.1'


class MailSender(object):
    """
    A robot who send mails in templates.
    """
    def __init__(self):
        """
        Init basic infomation of mail sender.
        """
        self.mail_host = "smtp.163.com"
        self.mail_user = "friederich"
        self.mail_pw = "monster1983"
        self.sender = "Friederich River<friederich@163.com>"
        self.reciever = []
        self.mail_template_path = '/opt/neutrino/template/'

    def smtp_config(self):
        try:
            smtp_server = smtplib.SMTP()
            smtp_server.connect(self.mail_host, 25)
            smtp_server.login(self.mail_user, self.mail_pw)
            return smtp_server
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    def smtp_ssl_config(self):
        try:
            smtp_server = smtplib.SMTP_SSL(self.mail_host,465)
            smtp_server.login(self.mail_user, self.mail_pw)
            return smtp_server
        except smtplib.SMTPException:
            raise smtplib.SMTPException

    def send(self, message):
        """
        Agent for sending mails.
        """
        try:
            smtp_server = self.smtp_ssl_config()
            smtp_server.sendmail(
                self.sender,
                message['To'].split(','),
                message.as_string())
            smtp_server.quit()
            # print('Success!')
        except smtplib.SMTPException as e:
            raise smtplib.SMTPException

    def mail_list(self):
        """
        Reciever list, reading from a config file.
        """
        self.reciever = [
            'Fred<hezhiyuan_tju@163.com>',
            'Guest<362381761@qq.com>']
        # self.reciever = ['Guest<hezhiyuan_tju@163.com>']

    def html_mail(self, reciever, mail_content):
        message = MIMEText(mail_content, 'html', 'utf-8')
        message['From'] = self.sender
        message['To'] = reciever
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def mail_generater(self, msg, reciever, mail_attachment=None):
        if isinstance(msg, MIMEText):
            msg['From'] = self.sender
            msg['To'] = reciever
            msg['Subject'] = Header(subject, 'utf-8')
        if isinstance(mail_attachment, list):
            for att in mail_attachment:
                msg.attach(att)
        elif mail_attachment:
            msg.attach(mail_attachment)


    def mail_content(self):
        """
        Mail template, title, content, etc.
        """
        # Friederich River<friederich@163.com>
        subject, mail_content = self.mail_daily_report('guest mail')
        message = MIMEText(mail_content, 'html', 'utf-8')
        message['From'] = self.sender
        message['To'] = ','.join(self.reciever)
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def template_list(self, jfile, tittle):
        result = None
        if os.path.exists(jfile):
            with open(jfile, 'r') as f:
                content = json.loads(f.read())
            for d in content:
                if d['subject'] == tittle:
                    result = d['subject'], d['template']
                    # here should be modified.
        else:
            result = None
        return result

    def mail_daily_report(self, subject):
        _, template_file = self.template_list('template/template_list.json', subject)
        with open(f"template/{template_file}", 'r') as f:
            content = f.read()
        return subject, content

    def mail_close_price(self):
        import datetime
        from email.mime.multipart import MIMEMultipart
        # Friederich River<friederich@163.com>
        message = MIMEMultipart()
        message.attach(MIMEText(f"Close price {datetime.date.today()}", 'plain', 'utf-8'))
        message['From'] = self.sender
        message['To'] = ','.join(self.reciever)
        message['Subject'] = Header(f"Close price {datetime.date.today()}", 'utf-8')
        #att3 = MIMEText(open('/home/fred/data.xls', 'rb').read()) 
        att3 = MIMEText(
            open('/home/friederich/Documents/dev/neutrino/applications/dist/data.xls', 'rb').read(),
            'base64', 'utf-8')
        att3["Content-Type"] = 'application/octet-stream' 
        att3.add_header('Content-Disposition','attachment',filename = f"close_price_{datetime.date.today()}.xls")
        message.attach(att3) 
        return message


class Mail(object):
    """
    A robot who send mails in templates.
    """
    def __init__(self):
        """
        Init basic infomation of mail sender.
        """
        self.sender = "Friederich River<friederich@163.com>"
        self.reciever = []
        self.mail_template_path = '/opt/neutrino/template/'

    def mail_list(self):
        """
        Reciever list, reading from a config file.
        """
        self.reciever = [
            'Guest<hezhiyuan_tju@163.com>',
            'Guest<362381761@qq.com>']
        self.reciever = ['Guest<hezhiyuan_tju@163.com>']

    def html_mail(self, reciever, mail_content):
        message = MIMEText(mail_content, 'html', 'utf-8')
        message['From'] = self.sender
        message['To'] = reciever
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def mail_generater(self, msg, reciever, mail_attachment=None):
        if isinstance(msg, MIMEText):
            msg['From'] = self.sender
            msg['To'] = reciever
            msg['Subject'] = Header(subject, 'utf-8')
        if isinstance(mail_attachment, list):
            for att in mail_attachment:
                msg.attach(att)
        elif mail_attachment:
            msg.attach(mail_attachment)


    def mail_content(self):
        """
        Mail template, title, content, etc.
        """
        # Friederich River<friederich@163.com>
        subject, mail_content = self.mail_daily_report('guest mail')
        message = MIMEText(mail_content, 'html', 'utf-8')
        message['From'] = self.sender
        message['To'] = ','.join(self.reciever)
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def template_list(self, jfile, tittle):
        result = None
        if os.path.exists(jfile):
            with open(jfile, 'r') as f:
                content = json.loads(f.read())
            for d in content:
                if d['subject'] == tittle:
                    result = d['subject'], d['template']
                    # here should be modified.
        else:
            result = None
        return result

    def mail_daily_report(self, subject):
        _, template_file = self.template_list('template/template_list.json', subject)
        with open(f"template/{template_file}", 'r') as f:
            content = f.read()
        return subject, content

    def mail_close_price(self):
        import datetime
        from email.mime.multipart import MIMEMultipart
        # Friederich River<friederich@163.com>
        message = MIMEMultipart()
        message.attach(MIMEText(f"Close price {datetime.date.today()}", 'plain', 'utf-8'))
        message['From'] = self.sender
        message['To'] = ','.join(self.reciever)
        message['Subject'] = Header(f"Close price {datetime.date.today()}", 'utf-8')
        #att3 = MIMEText(open('/home/fred/data.xls', 'rb').read()) 
        att3 = MIMEText(
            open('/home/friederich/Documents/dev/neutrino/applications/dist/data.xls', 'rb').read(),
            'base64', 'utf-8')
        att3["Content-Type"] = 'application/octet-stream' 
        att3.add_header('Content-Disposition','attachment',filename = f"close_price_{datetime.date.today()}.xls")
        message.attach(att3) 
        return message

def send_mail_to_chamber():
    Mercury = MailSender()
    Mercury.mail_list()
    Mercury.send(Mercury.mail_close_price())


if __name__ == "__main__":
    Mercury = MailSender()
    Mercury.mail_list()
    Mercury.send(Mercury.mail_close_price())
    # Mercury.send(Mercury.mail_content())
