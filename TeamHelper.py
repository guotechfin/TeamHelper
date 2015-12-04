# coding=gbk

import task
import os
from apscheduler.schedulers.blocking import BlockingScheduler


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(task.task_RetrieveWebsiteAndSendReport, 'cron', day_of_week='fri', hour=15, minute=46)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass