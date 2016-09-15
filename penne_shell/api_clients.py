import sys
import logging

import requests

from penne_shell import utils
from penne_shell import settings

logger = logging.getLogger(__name__)


class FrontDeskException(Exception):
    pass


class RequestException(FrontDeskException):
    pass


class FrontDesk(object):

    def __init__(self, host=settings.FRONTDESK_HOST):

        self._host = host

    def uploadfile(self, fl, depositor='anonymous'):
        endpoint = 'frontdesk/deposits/'

        flo = open(fl, 'rb')
        md5_sum = utils.safe_checksum_file(flo)
        files = {
            'package': flo
        }
        params = {
            'md5_sum': md5_sum,
            'depositor': depositor
        }
        url = 'http://%s/%s' % (self._host, endpoint)
        try:
            requests.post(
                url,
                data=params,
                files=files
            )
        except requests.exceptions.RequestException as exp:
            logger.exception(sys.exc_info()[0])
            raise RequestException("Request fail: %s (%s)" % (url, str(files.update(params))))
