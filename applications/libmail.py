#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header


__version__ = '1.0.1'


class MailSender(object):
    def __init__(self):
        self.mail_host = "smtp.163.com"
        self.mail_user = "friederich"
        self.mail_pw = "monster1983"
        self.sender = "Friederich River<friederich@163.com>"
        self.reciever = []

    def send(self, message):
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pw)
            smtpObj.sendmail(
                self.sender,
                message['To'].split(','),
                message.as_string())
            smtpObj.quit()
            print('Success!')
        except smtplib.SMTPException as e:
            print("Failed!", e)

    def mail_list(self):
        self.reciever = [
            'Guest<hezhiyuan_tju@163.com>',
            'Guest<362381761@qq.com>']
        self.reciever = ['Guest<hezhiyuan_tju@163.com>']

    def mail_content(self):
        # Friederich River<friederich@163.com>
        subject, mail_content = self.mail_daily_report()
        message = MIMEText(mail_content, 'html', 'utf-8')
        message['From'] = self.sender
        message['To'] = ','.join(self.reciever)
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def func1(self, jfile, tittle):
        if os.path.exist(jfile):
            with open(jfile, 'r') as f:
                content = json.loads(f.read())
            for d in content:
                if d['subject'] == tittle:
                    result = d['subject'], d['template_file']
                    # here should be modified.
        else:
            result = None
        return result

    def mail_daily_report(self, subject):
        template_file = template_list(subject)
        with open(f"template/{template_file}", 'r') as f:
            content = f.read()
        return subject, content


if __name__ == "__main__":
    Mercury = MailSender()
    Mercury.mail_list()
    Mercury.send(Mercury.mail_content())
