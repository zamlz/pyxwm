
import logging

class ColoredFormatter(logging.Formatter):

    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[%sm"

    color_map = {
        'DEBUG': '32',
        'INFO': '34',
        'WARNING': '33',
        'ERROR': '31',
        'CRITICAL': '34'
    }

    def __init__(self, *args, **kwargs):
        super(ColoredFormatter, self).__init__(*args, **kwargs)

    def format(self, record):

        if record.levelname in ColoredFormatter.color_map:
            name = record.levelname
            color = ColoredFormatter.color_map[record.levelname]
            record.levelname = ColoredFormatter.COLOR_SEQ % (color) \
                               + name + ColoredFormatter.RESET_SEQ

        result = super(ColoredFormatter, self).format(record)
        record.levelname = name
        return result


def dev_logging(log_name, log_level='INFO', console=False, filename=None):

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.getLevelName(log_level))
    format_str = ('[%(levelname)s] %(asctime)s [%(name)s] - '
                  '%(funcName)s:%(lineno)d > %(message)s')

    if console:
        sh = logging.StreamHandler()
        formatter = ColoredFormatter(format_str)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    if filename:
        fh = logging.FileHandler(filename)
        formatter = logging.Formatter(format_str)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
