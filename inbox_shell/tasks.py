# coding: utf-8
import sys
import os
import logging

from celery import Celery
from celery.utils.log import get_task_logger

from inbox_shell.api_clients import FrontDesk
from inbox_shell import settings

logger = get_task_logger(__name__)

celery_broker = 'amqp://%s//' % settings.RABBITMQ_HOST
app = Celery('tasks', broker=celery_broker)

fd = FrontDesk()

logger.info("Running in safe mode: %s" % settings.SAFE_MODE)
logger.info("Logging level: %s" % settings.LOGGING_LEVEL)
logger.info("FRONTDESK Deposit host: %s" % settings.FRONTDESK_HOST)


@app.task
def uploadfile(filename, depositor, safe_mode):
    logger.info('Scheduling file to be sent: %s', filename)

    try:
        fd.uploadfile(filename, depositor)
    except Exception:
        logger.exception(sys.exc_info()[0])

    if safe_mode:  # skiping to remove files from server.
        return

    os.remove(filename)
