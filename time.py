# coding=gbk

import time
from datetime import datetime

print time.localtime()


def getWeekNo():
    date1 = datetime.strptime('2015-9-14','%Y-%m-%d')
    date2 = datetime.now()
    days = int((date2 - date1).total_seconds() / 24 / 3600)
    return days / 7 + 1

def getWeekDay():
    date1 = datetime.strptime('2015-9-14','%Y-%m-%d')
    date2 = datetime.now()
    days = int((date2 - date1).total_seconds() / 24 / 3600)
    return days % 7 + 1

if __name__ == '__main__':
    print "Week No: %s, Week Day: %s" % (getWeekNo(), getWeekDay())