#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = "friederich"
mail_pass = "monster1983"

sender = 'Friederich River<friederich@163.com>'
reciever = ['Guest<hezhiyuan_tju@163.com>','Guest<362381761@qq.com>']
# Friederich River<friederich@163.com>
with open('template/guest_mail.html', 'r') as f:
    mail_content = f.read()
message = MIMEText(mail_content, 'html', 'utf-8')
message['From'] = sender
message['To'] = ','.join(reciever)
subject = 'Guten Tag'
message['Subject'] = Header(subject, 'utf-8')
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, message['To'].split(','), message.as_string())
    smtpObj.quit()
    print('Success!')
except smtplib.SMTPException as e:
    print('Failed.', e)
