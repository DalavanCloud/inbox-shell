# coding: utf-8

import click
import logging
import logging.config

from inbox_shell.shell import monitor
from inbox_shell import settings

logger = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'inbox_shell': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}


def _config_logging(logging_level='DEBUG'):

    LOGGING['loggers']['inbox_shell']['level'] = logging_level

    logging.config.dictConfig(LOGGING)


@click.command()
@click.argument('monitored_path', default=settings.MONITORING_FOLDER)
@click.option('--safe_mode', '-s', is_flag=True)
@click.option(
    '--logging_level', '-l', default=settings.LOGGING_LEVEL,
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
)
def main(monitored_path, safe_mode, logging_level):

    if not safe_mode and settings.SAFE_MODE:
        safe_mode = True

    _config_logging(logging_level=logging_level)

    logger.info("Running in safe mode: %s" % safe_mode)
    logger.info("Logging level: %s" % settings.LOGGING_LEVEL)
    monitor(monitored_path, safe_mode=safe_mode)

if __name__ == "__main__":
    main()
