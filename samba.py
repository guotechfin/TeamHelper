# coding=gbk

from smb.SMBConnection import SMBConnection

import week_time
import os

try:
    import user_data
    smb_credential = user_data.smb_credential
except:
    smb_credential = {'host': 'something.com', 'hostname': 'myhost', 'user': 'test', 'password': '123'}

def getFileList():
    filename_list = []
    conn = SMBConnection(smb_credential['user'], smb_credential['password'], "", smb_credential['hostname'], use_ntlm_v2 = True)
    conn.connect(smb_credential['host'], 139)

    file_list = conn.listPath('OSV', u'/Audit/每周会议记录/OSVT-16年秋季学期会议记录')
    for f in file_list:
        if f.filename != '.' and f.filename != '..':
            filename_list.append(f.filename)

    conn.close()
    return filename_list

def check_meeting_record():
    res = False
    search_str = u'第%d周会议记录' % (week_time.getWeekNo())
    filename_list = getFileList()
    print 'Meeting records:'
    for filename in filename_list:
        print filename
        if filename.find(search_str) != -1:
            res = True
    print 'Need to find: ' + search_str
    if res:
        print 'Already Found!'
    else:
        print 'Not Found!'
    return res


if __name__ == '__main__':
    res = check_meeting_record()