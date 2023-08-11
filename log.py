import logging
import coloredlogs

def get_logger_instance():
    if not hasattr(get_logger_instance, 'instance'):
        logger = logging.getLogger()
        coloredlogs.install(level=logging.DEBUG, logger=logger)
        get_logger_instance.instance = logger
    return get_logger_instance.instance