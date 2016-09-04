# coding=gbk

import qq
import database
import week_time
import mail
import samba

try:
    import user_data
    user_list = user_data.user_list
    record_list = user_data.record_list
except:
    print 'No user data, use default value'
    user_list = {}
    user_list['ly'] = {'name': 'ly', 'email': 'xxx@something.com', 'spell': 'osvtzhuli'}
    record_list = ['ly']


def analyzeProgress(str):
    res = ''
    if str.find(u'û�а�ʱд���´�ע��') != -1:
        res = u'���Ԥ��δ��д��'
    elif len(str) == 0:
        res = u'���Ԥ��δ��д��'
    elif len(str) < 8:
        res = u'���Ԥ�泤�ȹ��̣�����8���֣�'
    else:
        res = u''
    # print "Text: %s, Result: %s" %(str, res)
    return res

def printRemarks():
    for name in user_list.keys():
        info = user_list[name]
        print "%s ||| %s ||| %s" % (info['cname'], info['progress'], info['remark'])


def performEvaluation():
    name_progress = database.analyzeMeetingInfo(database.getMeetingInfo())
    # print '\n'.join(name_progress)

    for name in user_list.keys():
        info = user_list[name]
        info['remark'] = u''

    print ''
    for cname in name_progress.keys():
        progress = name_progress[cname]
        for name in user_list.keys():
            info = user_list[name]
            if info['cname'] == cname:
                info['progress'] = progress
                info['remark'] = analyzeProgress(progress)
    printRemarks()

def generateQQMeetingReport():
    has_issue = 0
    text = u'��Һã�Ŀǰ���Ԥ�滹��Щ���⣬�������ƺ��ύ��http://osvt.net:9000/p/meeting��\n'
    for name in user_list.keys():
        info = user_list[name]
        if info['remark'] != '':
            text = text + u'@' + info['name'] + u'��' + info['remark'] + '\n'
            has_issue = 1
    if has_issue == 0:
        text = 'OK'
    print 'Meeting Report:\n' + text
    return text

def getRecordPerson():
    return record_list[week_time.getWeekNo() % len(record_list)]

def getLastRecordPerson():
    return record_list[(week_time.getWeekNo() - 1) % len(record_list)]

def generateQQMeetingNotice():
    text = u'��Һã���ᶨ�����ܶ�����9:30�ٿ�������ʦ���ϯ�������ֵ�'
    for name in user_list.keys():
        info = user_list[name]
        if info['type'] == week_time.getWeekNo() % 2:
            text = text + u'@' + info['name']
    text = text + u'�����˿��н�չ&˼·�㱨��ÿ�˰ѻ㱨��Ҫ����Ŀ�������ã��ʼ����ã���ֹ��������22:00������ַ��http://osvt.net:9000/p/meeting'
    text = text + u'�������ֵ�@' + getRecordPerson() + u'�������¼�����������������ύ����\\\\osvt.net\\osv\\Audit\\ÿ�ܻ����¼\\OSVT-16�괺��ѧ�ڻ����¼'
    print 'Meeting Notice:\n' + text
    return text

def generateQQRecordNotice():
    text = u'��Һã���������ѽ����������¼��@' + getLastRecordPerson() + u'�����������22:00֮ǰ�ύ����\\\\osvt.net\\osv\\Audit\\ÿ�ܻ����¼\\OSVT-16�괺��ѧ�ڻ����¼'
    print 'Record Notice:\n' + text
    return text

def generateQQRecordReport():
    text = u'��Һã�Ŀǰ�������¼��δ�ύ��@' + getLastRecordPerson() + u'����������ύ����\\\\osvt.net\\osv\\Audit\\ÿ�ܻ����¼\\OSVT-16�괺��ѧ�ڻ����¼'
    print 'Record Report:\n' + text
    return text

def generateMailTitleAndContent():
    close = u'''


--
                      ��
��

admin@osvt.net
����ϵͳ�����⻯��Ŀ��
������ѧ�����΢����ѧԺ
'''
    title = '������ϵͳ�����⻯��2016���＾ѧ�ڵ�%d����᡿֪ͨ������Ԥ��' % (week_time.getWeekNo() + 1)
    content = database.getMeetingInfo() + close
    return (title, content)

def addMeetingRemarksToMail(str):
    for name in user_list.keys():
        info = user_list[name]
        if info['remark'] != u'':
            pos = str.find(info['cname'] + u'��')
            if pos == -1:
                continue
            pos = str.find('\n', pos)
            if pos == -1:
                continue
            str = str[:pos] + u' ��' + info['remark'] + u'��' + str[pos:]
    return str

def addRecordRemarkToMail(str):
    if samba.check_meeting_record() == True:
        return str
    info = user_list[getLastRecordPerson()]
    str = str.replace(u'ÿ�˲�����40���ӡ�', u'ÿ�˲�����40���ӡ����⣬�����������¼��δ�ύ����' + info['cname'] + u'�����ύ��')
    return str

def task_SendQQMeetingNotice():
    notice = generateQQMeetingNotice()
    qq.QQ_SendTextWithAt(notice)

def task_SendQQRecordNotice():
    notice = generateQQRecordNotice()
    qq.QQ_SendTextWithAt(notice)

def task_RetrieveWebsiteAndSendQQReport():
    performEvaluation()
    report = generateQQMeetingReport()
    if report != 'OK':
        qq.QQ_SendTextWithAt(report)

def task_RetrieveRecordAndSendQQReport():
    if samba.check_meeting_record() == False:
        report = generateQQRecordReport()
        qq.QQ_SendTextWithAt(report)

def task_SendNextMeetingMails():
    performEvaluation()
    (title, content) = generateMailTitleAndContent()
    content = addMeetingRemarksToMail(content)
    content = addRecordRemarkToMail(content)
    print 'Title:\n' + title
    print 'Content:\n' + content
    mail.mail_sendMails(title, content)


if __name__ == '__main__':
    # task_SendQQMeetingNotice()
    # task_RetrieveWebsiteAndSendQQReport()
    # task_SendNextMeetingMails()
    print week_time.getWeekNo()
    print getLastRecordPerson()

    text = ''
    for name in user_list.keys():
        info = user_list[name]
        if info['type'] == week_time.getWeekNo() % 2:
            text = text + u'@' + info['name']
    print text

    # task_SendQQRecordNotice()
    # task_RetrieveRecordAndSendQQReport()
