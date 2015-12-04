# coding=gbk

import smtplib
from email.mime.text import MIMEText

try:
    import user_data
    mail_credential = user_data.mail_credential
    receive_list = user_data.receive_list
    copy_list = user_data.copy_list
except:
    print 'No user data, use default value'
    mail_credential = {'address': 'xxx@something.com', 'password': '123'}
    receive_list=['receive@something.com']
    copy_list=['cc@qq.something.com']


def send_mails(cred, receive_list, copy_list, sub, content):
    mail_address = cred['address']
    mail_pass = cred['password']
    mail_host = mail_address.split('@')[1]

    me = "OSVT项目组助理" + "<" + mail_address + ">"
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(receive_list)
    msg['Cc'] = ";".join(copy_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_address, mail_pass)
        server.sendmail(me, receive_list + copy_list, msg.as_string())
        server.quit()
        return True
    except Exception, e:
        print str(e)
        return False

def mail_sendMails(title, content):
    send_mails(mail_credential, receive_list, copy_list, title, content)

# send_mail(mail_credential, receive_list, copy_list, "Title", "hello world！")


if __name__ == '__main__':
    week_no = 12
    title = '【操作系统与虚拟化组第WEEK_NO周组会】通知与内容预告'
    content = '''各位老师、同学好：
    本组第WEEK_NO周组会于下周二（后天）上午9:30召开，地点中科院实验室291，所有组员进行个人工作的PPT汇报，每人不超过20分钟。

   罗杨：1）完成AsiaCCS'16投稿；2）推进patron的工程进展。
   陈康：**没有按时写，下次注意**
   孙茜：**没有按时写，下次注意**
   罗武：ra进展
   周鸿博：没有太多要讲，上周期中大作业和1/2的专题
   刘威：OpenStack消息通信机制
   濮阳天：**没有按时写，下次注意**


--
                      致
礼！

admin@osvt.net
操作系统与虚拟化项目组
北京大学软件与微电子学院
'''
    title = title.replace('WEEK_NO', str(week_no))
    content = content.replace('WEEK_NO', str(week_no))
    mail_sendMails(title, content)
