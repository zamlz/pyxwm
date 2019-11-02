
import logging

def dev_logging(log_name, log_level='INFO', console=False, filename=None):

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.getLevelName(log_level))

    if console:
        sh = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    if filename:
        fh = logging.FileHandler(filename)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
