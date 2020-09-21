#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: LBotCoreBackend.py
@time: 2020/6/11 15:14
@desc:
'''


from django.core.management.base import BaseCommand
from Botend.views import LBotCoreBackend

from utils.log import logger

import sys
import traceback
from queue import Queue, Empty


class Command(BaseCommand):
    help = 'bot backend'

    def handle(self, *args, **options):

        try:
            LBotCoreBackend()

        except KeyboardInterrupt:
            logger.warn("[Bot] stop bot.")
            exit(0)
        except:
            logger.error("[Bot] something error, {}".format(traceback.format_exc()))
