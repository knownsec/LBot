#!/usr/bin/env python
# encoding: utf-8


import time
import traceback

from utils.LReq import LReq
from utils.log import logger
from core.threadingpool import ThreadPool

from Botend.models import ReportTask
from LBot.settings import CTF_BACK_COOKIE


class LBotCoreBackend:
    """
    bot 守护线程
    """
    def __init__(self):
        # 任务与线程分发
        self.threadpool = ThreadPool()

        ReportTasks = ReportTask.objects.filter(aread=0).count()
        left_tasks = ReportTasks

        logger.info("[LBot Main] Bot Backend Start...now {} targets left.".format(left_tasks))

        # 获取线程池然后分发信息对象
        # 当有空闲线程时才继续
        i = 0

        while 1:
            while self.threadpool.get_free_num():

                if i > 20:
                    logger.warning("[LBot Core] More than 20 thread init. stop new Thread.")
                    self.threadpool.wait_all_thread()
                    break

                else:
                    i += 1
                    botcore = LBotCore()

                    logger.debug("[LBot Core] New Thread {} for LBot Core.".format(i))

                    self.threadpool.new(botcore.scan)
                    time.sleep(0.5)

            # self.threadpool.wait_all_thread()
            time.sleep(1)


class LBotCore:
    """
    bot 主线程
    """

    def scan(self):

        while 1:

            try:
                # sleep
                time.sleep(3)

                reportt = ReportTask.objects.filter(aread=0).first()

                if not reportt:
                    continue

                reportt.aread = 1
                reportt.save()

                report_url = reportt.url
                cookies = "admin="+CTF_BACK_COOKIE

                self.req = LReq(is_chrome=True)

                self.req.get(report_url, 'RespByChrome', 0, cookies)

                # self.req.close_driver()

            except KeyboardInterrupt:
                logger.error("[Scan] Stop Scaning.")
                self.req.close_driver()
                exit(0)

            except:
                logger.warning('[Scan] something error, {}'.format(traceback.format_exc()))
                raise