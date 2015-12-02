# coding=gbk

import MySQLdb

try:
    import user_data
    db_credential = user_data.db_credential
except:
    print 'No user data, use default value'
    db_credential = {'host': 'something.com', 'user': 'xxx', 'password': '123', 'database': 'xxx'}



conn = MySQLdb.connect(
    host = db_credential['host'],
    user = db_credential['user'],
    passwd = db_credential['password'],
    db = db_credential['database'],
)

cursor = conn.cursor()
sql = 'SELECT * FROM store'

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print row

except Exception, e:
    print e

conn.close()