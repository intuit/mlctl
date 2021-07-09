import logging
import click


class Logger:
    logger = None

    def __init__(self):
        pass

    @classmethod
    def get_level(cls, level):
        if level == "CRITICAL":
            return logging.CRITICAL
        elif level == "ERROR":
            return logging.ERROR
        elif level == "WARNING":
            return logging.WARNING
        elif level == "INFO":
            return logging.INFO
        elif level == "DEBUG":
            return logging.DEBUG
        else:
            return logging.NOTSET

    @classmethod
    def configure(cls, loglevel="INFO"):
        # reduce informational logging
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        # initialize class logger
        cls.logger = logging.getLogger('mlctl')
        cls.logger.setLevel(logging.DEBUG)

        # set a format which is simpler for console use
        consoleHandlerFormatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
        # define a Handler which writes sys.stdout
        consoleHandler = logging.StreamHandler()
        # Set log level
        consoleHandler.setLevel(cls.get_level(loglevel))

        # tell the handler to use this format
        consoleHandler.setFormatter(consoleHandlerFormatter)
        # add the handler to the root logger
        cls.logger.addHandler(consoleHandler)

    @classmethod
    def debug(cls, str):
        cls.logger.debug(str)

    @classmethod
    def info(cls, str):
        cls.logger.info(str)

    @classmethod
    def warning(cls, str):
        cls.logger.warning(str)

    @classmethod
    def error(cls, str):
        cls.logger.error(str)

    @classmethod
    def critical(cls, str):
        cls.logger.critical(str)


def enable_verbose_option(**kwargs):
    kwargs.setdefault('help', 'Enables verbose mode')
    kwargs.setdefault('is_flag', True)
    names = ['--verbose', '-v']

    def decorator(f):
        def _set_level(ctx, param, value):
            if value:
                Logger.configure('DEBUG')
            else:
                Logger.configure('INFO')
        return click.option(*names, callback=_set_level, **kwargs)(f)
    return decorator