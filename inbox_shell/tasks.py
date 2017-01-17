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


@app.task
def uploadfile(filename, depositor):
    logger.info('Scheduling file to be sent: %s', filename)

    try:
        fd.uploadfile(filename, depositor)
    except Exception:
        logger.exception(sys.exc_info()[0])
    finally:
        if settings.SAFE_MODE:  # skiping to remove files from server.
            return
        os.remove(filename)
