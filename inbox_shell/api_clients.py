import sys
import logging

import requests

from inbox_shell import utils
from inbox_shell import settings

logger = logging.getLogger(__name__)


class FrontDeskException(Exception):
    pass


class RequestException(FrontDeskException):
    pass


class FrontDesk(object):

    def __init__(self, host=settings.FRONTDESK_HOST):

        self._host = host

    def uploadfile(self, fl, depositor='anonymous'):
        logger.info('Starting file deposit: (%s)' % fl)
        flo = open(fl, 'rb')
        md5_sum = utils.safe_checksum_file(flo)
        files = {
            'package': flo
        }
        params = {
            'md5_sum': md5_sum,
            'depositor': depositor
        }
        url = '%s/frontdesk/deposits/' % (self._host)
        try:
            result = requests.post(
                url,
                data=params,
                files=files
            )

            if result.status_code not in [200, 300]:
                raise RequestException(
                    "Request fail: %s (%s) %d" % (
                        url,
                        str(files.update(params)),
                        result.status_code
                    )
                )

            logger.info('File deposited: (%s)' % fl)
        except requests.exceptions.RequestException:
            logger.error('File could not be deposited: (%s)' % fl)
            logger.exception(sys.exc_info()[0])
            raise RequestException(
                "Request fail: %s (%s)" % (url, str(files.update(params)))
            )
