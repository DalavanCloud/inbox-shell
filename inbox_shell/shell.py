# coding: utf-8
import logging
import zipfile
import time
import datetime
import sys
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from inbox_shell import tasks
from inbox_shell import settings

logger = logging.getLogger(__name__)


class Inspector(object):
    """
    Essa classe contém um conjunto de validações de integridade do arquivo zip e
    validações de nome dos arquivos zip.
    """

    def __init__(self, filename):
        logger.info('Inspecting file: %s', filename)

        self._file = filename
        self._filename = filename.split('/')[-1]

    def _is_valid_zip(self):
        """
        Esse método verifica se o arquivo zip é válido.
        """
        return zipfile.is_zipfile(self._file)

    def _is_valid_filename(self):
        """
        Esse método valida o nome do arquivo zip de acordo com a regra:
        issn-acronimo_revista-volume-número-página.zip.
        """
        return True

    def is_valid(self):

        if not self._is_valid_zip():
            return (False, 'invalid zip')

        return (True, 'zip file is valid')


class EventHandler(FileSystemEventHandler):

    logfilename = 'report.log'

    def __init__(self, directory, safe_mode=settings.SAFE_MODE):
        self._safe_mode = safe_mode
        self._files = {}
        self.depositor = directory.split('/')[-1]

    def is_file_size_stucked(self, logpath):
        status = self._files.setdefault(logpath, 0)
        current = os.path.getsize(logpath)
        if not status == current:
            self._files[logpath] = current
            return False
        del(self._files[logpath])
        return True

    def write_log(self, logpath, message):

        logpath = logpath.split('/')
        logpath[-1] = self.logfilename
        logfile = '/'.join(logpath)

        message = datetime.datetime.now().isoformat()[:19] + ' - ' + message

        with open(logfile, 'a') as f:
            line = '%s\r\n' % message
            f.write(line)

    def on_created(self, event):

        if self.logfilename in event.src_path:
            return False

        try:
            if event.is_directory:
                msg = 'New directory detected: %s' % event.src_path
                logger.debug(msg)
                self.write_log(event.src_path, msg)
                if self._safe_mode:  # skiping to remove data from FTP.
                    msg = 'Directory is not valid it will be skipped: %s' % event.src_path
                    logger.debug(msg)
                    self.write_log(event.src_path, msg)
                    return False
                os.rmdir(event.src_path)
                msg = 'Directory removed: %s' % event.src_path
                logger.debug(msg)
                self.write_log(event.src_path, msg)
                return False

            msg = 'New file detected: %s' % event.src_path
            logger.info(msg)
            self.write_log(event.src_path, msg)

            while True:
                msg = 'File is being uploaded to the FTP: %s' % event.src_path
                logger.info(msg)
                self.write_log(event.src_path, msg)
                if self.is_file_size_stucked(event.src_path):
                    break
                time.sleep(10)

            inspector = Inspector(event.src_path)
            validated, validation_message = inspector.is_valid()
            msg = "Is this file valid: %s" % str(validated)
            logger.debug(msg)

            if validated:
                msg = "File is valid, sending for processing: %s" % event.src_path
                logger.debug(msg)
                self.write_log(event.src_path, msg)
                tasks.uploadfile.delay(event.src_path, self.depositor)
                return None

            if self._safe_mode:  # skiping to remove data from FTP.
                msg = 'File is not valid it will be skipped: %s' % event.src_path
                logger.debug(msg)
                self.write_log(event.src_path, msg)
                return False

            os.remove(event.src_path)
            msg = "File is not valid (%s), removed from server: %s" % (
                validation_message, event.src_path)
            logger.debug(msg)
            self.write_log(event.src_path, msg)

        except Exception:
            logger.exception(sys.exc_info()[0])
            return None


def monitor(monitored_path, safe_mode=settings.SAFE_MODE):
    """
    Monitor inicia instancias de observadores de mudanças em diretórios.

    :param monitored_path:
        Path absoluto para o diretório root do FTP server, neste diretório devem
        conter os diretórios das contas de FTP dos usuários do FTP.
    :type path:
        ``str``

    :param safe_mode:
        Indica aos monitores se os arquivos e diretórios criados fora de
        conformidade com o padrão aceito, podem ser removidos do FTP.
        Quando definido como True os arquivos fora de conformidade são
        preservados
    :type path:
        ``bool``

    :return:
        ``None``
    """
    try:
        directories_in_ftp_root_dir = [os.path.join(monitored_path, name) for name in os.listdir(monitored_path) if os.path.isdir(os.path.join(monitored_path, name)) ]
    except FileNotFoundError:
        logger.error('Directory not found: %s', monitored_path)
        logger.error('Monitor is shutting down')
        return None

    for directory in directories_in_ftp_root_dir:
        event_handler = EventHandler(directory, safe_mode=safe_mode)
        observer = Observer()
        observer.schedule(
            event_handler, directory, recursive=False
        )
        logger.info('Starting to monitor for the directory: %s', directory)
        observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
