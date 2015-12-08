# coding=gbk

import task
import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler


if __name__ == '__main__':
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    print time.strftime(ISOTIMEFORMAT, time.localtime())

    scheduler = BlockingScheduler()
    scheduler.add_job(task.task_SendQQMeetingNotice,            'cron', day_of_week='fri', hour=20, minute=0)
    scheduler.add_job(task.task_RetrieveWebsiteAndSendQQReport, 'cron', day_of_week='sun', hour=12, minute=0)
    scheduler.add_job(task.task_RetrieveWebsiteAndSendQQReport, 'cron', day_of_week='sun', hour=20, minute=0)
    scheduler.add_job(task.task_RetrieveWebsiteAndSendQQReport, 'cron', day_of_week='sun', hour=21, minute=55)
    scheduler.add_job(task.task_SendNextMeetingMails,           'cron', day_of_week='sun', hour=22, minute=0)
    scheduler.add_job(task.task_SendQQRecordNotice,             'cron', day_of_week='tue', hour=14, minute=0)

    # just for test
    # scheduler.add_job(task.task_RetrieveWebsiteAndSendQQReport, 'interval', seconds=5)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass