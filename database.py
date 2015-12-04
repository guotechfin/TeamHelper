# coding=gbk

import MySQLdb
import re
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

try:
    import user_data
    db_credential = user_data.db_credential
except:
    print 'No user data, use default value'
    db_credential = {'host': 'something.com', 'user': 'xxx', 'password': '123', 'database': 'xxx'}


def getMeetingInfo():
    name_progress = {}
    conn = MySQLdb.connect(
        host = db_credential['host'],
        user = db_credential['user'],
        passwd = db_credential['password'],
        db = db_credential['database'],
        charset = "utf8"
    )

    cursor = conn.cursor()
    sql = "SELECT * FROM store WHERE `key`='pad:meeting'"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            p = re.compile('"text":"(.*)","attribs"')
            m = p.search(row[1])
            if m:
                str = m.group(1).replace('\\n', '\n')
                str = str[str.rfind('-----') + 5:].strip()
                # print 'Meeting info from website:\n' + str
                return str
    except Exception, e:
        print e
        return ''

    conn.close()
    return ''


def analyzeMeetingInfo(str):
    name_progress = {}
    p = re.compile(u' ([\u4E00-\u9FA5]{2,3})[：:](.*)')
    m = p.findall(str)
    for item in m:
        print "name = %s, progress = %s" % (item[0], item[1])
        name_progress[item[0]] = item[1]
    return name_progress

if __name__ == '__main__':
    name_progress = analyzeMeetingInfo(getMeetingInfo())
    print '\n'.join(name_progress)