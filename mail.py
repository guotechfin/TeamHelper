# coding=gbk

import smtplib
from email.mime.text import MIMEText

try:
    import user_data
    mail_credential = user_data.mail_credential
except:
    print 'No user data, use default value'
    mail_credential = {'address': 'xxx@something.com', 'password': '123'}


receive_list=['admin@osvt.net', 'hsluoyz@qq.com']

def send_mail(cred, receive_list, sub, content):
    mail_address = cred['address']
    mail_pass = cred['password']
    mail_host = mail_address.split('@')[1]

    me = "admin" + "<" + mail_address + ">"
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(receive_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_address, mail_pass)
        server.sendmail(me, receive_list, msg.as_string())
        server.quit()
        return True
    except Exception, e:
        print str(e)
        return False

send_mail(mail_credential, receive_list, "Title", "hello world！")

