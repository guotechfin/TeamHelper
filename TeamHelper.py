# coding=gbk

import qq
import database

try:
    import user_data
    user_list = user_data.user_list
except:
    print 'No user data, use default value'
    user_list = {}
    user_list['ly'] = {'name': 'ly', 'email': 'xxx@something.com', 'spell': 'osvtzhuli'}


def analyzeProgress(str):
    res = ''
    if str.find(u'û�а�ʱд���´�ע��') != -1:
        res = u'���Ԥ��δ��д��'
    elif len(str) < 8:
        res = u'���Ԥ�泤�ȹ��̣�����8���֣�'
    else:
        res = ''
    # print "Text: %s, Result: %s" %(str, res)
    return res

def printRemarks():
    for name in user_list.keys():
        info = user_list[name]
        print "%s ||| %s ||| %s" % (info['cname'], info['progress'], info['remark'])


def performEvaluation():
    name_progress = database.getMeetingInfo()
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
    text = u'��Һã�Ŀǰ���Ԥ�滹��Щ���⣬�������ƺ��ύ��http://osvt.net:9000/p/meeting��\n'
    for name in user_list.keys():
        info = user_list[name]
        if info['remark'] != '':
            text = text + u'@' + info['name'] + u'��' + info['remark'] + '\n'
    print 'Report:\n' + text
    return text

performEvaluation()
report = generateQQReport()
qq.QQ_SendTextWithAt(report)