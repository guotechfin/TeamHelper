# coding=gbk

import qq
import database
import week_time
import mail

try:
    import user_data
    user_list = user_data.user_list
except:
    print 'No user data, use default value'
    user_list = {}
    user_list['ly'] = {'name': 'ly', 'email': 'xxx@something.com', 'spell': 'osvtzhuli'}


def analyzeProgress(str):
    res = ''
    if str.find(u'没有按时写，下次注意') != -1:
        res = u'组会预告未填写！'
    elif len(str) < 8:
        res = u'组会预告长度过短，至少8个字！'
    else:
        res = ''
    # print "Text: %s, Result: %s" %(str, res)
    return res

def printRemarks():
    for name in user_list.keys():
        info = user_list[name]
        print "%s ||| %s ||| %s" % (info['cname'], info['progress'], info['remark'])


def performEvaluation():
    name_progress = database.analyzeMeetingInfo(database.getMeetingInfo())
    # print '\n'.join(name_progress)

    print ''
    for cname in name_progress.keys():
        progress = name_progress[cname]
        for name in user_list.keys():
            info = user_list[name]
            if info['cname'] == cname:
                info['progress'] = progress
                info['remark'] = analyzeProgress(progress)
    printRemarks()

def generateQQReport():
    text = u'大家好，目前组会预告还有些问题，请大家完善后提交到http://osvt.net:9000/p/meeting：\n'
    for name in user_list.keys():
        info = user_list[name]
        if info['remark'] != '':
            text = text + u'@' + info['name'] + u'：' + info['remark'] + '\n'
    print 'Report:\n' + text
    return text

def generateQQMeetingNotice():
    text = u'大家好，组会定于下周二上午9:30召开，沈老师会出席，本周轮到'
    for name in user_list.keys():
        info = user_list[name]
        if info['type'] == week_time.getWeekNo() % 2:
            text = text + u'@' + info['name']
    text = text + u'做个人科研进展&思路汇报。每人把汇报概要在项目组官网填好，邮件里用，截止到周日晚22:00），网址：http://osvt.net:9000/p/meeting'
    print 'Notice:\n' + text
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
    title = '【操作系统与虚拟化组第%d周组会】通知与内容预告' % (week_time.getWeekNo() + 1)
    content = database.getMeetingInfo() + close
    print 'Title:\n' + title
    print 'Content:\n' + content
    return (title, content)


def task_RetrieveWebsiteAndSendQQReport():
    performEvaluation()
    report = generateQQReport()
    qq.QQ_SendTextWithAt(report)

def task_SendQQMeetingNotice():
    notice = generateQQMeetingNotice()
    qq.QQ_SendTextWithAt(notice)

def task_SendNextMeetingMails():
    (title, content) = generateMailTitleAndContent()
    mail.mail_sendMails(title, content)


if __name__ == '__main__':
    # task_RetrieveWebsiteAndSendQQReport()
    # task_SendQQMeetingNotice()
    task_SendNextMeetingMails()
