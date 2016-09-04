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
    if str.find(u'没有按时写，下次注意') != -1:
        res = u'组会预告未填写！'
    elif len(str) == 0:
        res = u'组会预告未填写！'
    elif len(str) < 8:
        res = u'组会预告长度过短，至少8个字！'
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
    text = u'大家好，目前组会预告还有些问题，请大家完善后提交到http://osvt.net:9000/p/meeting：\n'
    for name in user_list.keys():
        info = user_list[name]
        if info['remark'] != '':
            text = text + u'@' + info['name'] + u'：' + info['remark'] + '\n'
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
    text = u'大家好，组会定于下周二上午9:30召开，沈老师会出席，本周轮到'
    for name in user_list.keys():
        info = user_list[name]
        if info['type'] == week_time.getWeekNo() % 2:
            text = text + u'@' + info['name']
    text = text + u'做个人科研进展&思路汇报。每人把汇报概要在项目组官网填好（邮件里用，截止到周日晚22:00），网址：http://osvt.net:9000/p/meeting'
    text = text + u'，本周轮到@' + getRecordPerson() + u'做会议记录，组会结束后两天内提交至：\\\\osvt.net\\osv\\Audit\\每周会议记录\\OSVT-16年春季学期会议记录'
    print 'Meeting Notice:\n' + text
    return text

def generateQQRecordNotice():
    text = u'大家好，本周组会已结束，会议记录由@' + getLastRecordPerson() + u'整理后，周三晚22:00之前提交至：\\\\osvt.net\\osv\\Audit\\每周会议记录\\OSVT-16年春季学期会议记录'
    print 'Record Notice:\n' + text
    return text

def generateQQRecordReport():
    text = u'大家好，目前组会会议记录仍未提交，@' + getLastRecordPerson() + u'尽快整理后，提交至：\\\\osvt.net\\osv\\Audit\\每周会议记录\\OSVT-16年春季学期会议记录'
    print 'Record Report:\n' + text
    return text

def generateMailTitleAndContent():
    close = u'''


--
                      致
礼！

admin@osvt.net
操作系统与虚拟化项目组
北京大学软件与微电子学院
'''
    title = '【操作系统与虚拟化组2016年秋季学期第%d周组会】通知与内容预告' % (week_time.getWeekNo() + 1)
    content = database.getMeetingInfo() + close
    return (title, content)

def addMeetingRemarksToMail(str):
    for name in user_list.keys():
        info = user_list[name]
        if info['remark'] != u'':
            pos = str.find(info['cname'] + u'：')
            if pos == -1:
                continue
            pos = str.find('\n', pos)
            if pos == -1:
                continue
            str = str[:pos] + u' （' + info['remark'] + u'）' + str[pos:]
    return str

def addRecordRemarkToMail(str):
    if samba.check_meeting_record() == True:
        return str
    info = user_list[getLastRecordPerson()]
    str = str.replace(u'每人不超过40分钟。', u'每人不超过40分钟。另外，上周组会会议记录还未提交，请' + info['cname'] + u'尽快提交。')
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
