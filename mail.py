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

    me = "OSVT��Ŀ������" + "<" + mail_address + ">"
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

# send_mail(mail_credential, receive_list, copy_list, "Title", "hello world��")


if __name__ == '__main__':
    week_no = 12
    title = '������ϵͳ�����⻯���WEEK_NO����᡿֪ͨ������Ԥ��'
    content = '''��λ��ʦ��ͬѧ�ã�
    �����WEEK_NO����������ܶ������죩����9:30�ٿ����ص��п�Ժʵ����291��������Ա���и��˹�����PPT�㱨��ÿ�˲�����20���ӡ�

   ���1�����AsiaCCS'16Ͷ�壻2���ƽ�patron�Ĺ��̽�չ��
   �¿���**û�а�ʱд���´�ע��**
   ���磺**û�а�ʱд���´�ע��**
   ���䣺ra��չ
   �ܺ販��û��̫��Ҫ�����������д���ҵ��1/2��ר��
   ������OpenStack��Ϣͨ�Ż���
   ����죺**û�а�ʱд���´�ע��**


--
                      ��
��

admin@osvt.net
����ϵͳ�����⻯��Ŀ��
������ѧ�����΢����ѧԺ
'''
    title = title.replace('WEEK_NO', str(week_no))
    content = content.replace('WEEK_NO', str(week_no))
    mail_sendMails(title, content)
