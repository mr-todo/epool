from logging.config import dictConfig


def init_logger(log_file, level='DEBUG'):
    conf = {
        'version': 1,
        'formatters': {
            'f': {
                'format': '%(asctime)s, %(levelname)s, %(name)s, %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': level,
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': level,
                'formatter': 'f',
                'filename': log_file,
                'backupCount': 15,
                'when': 'midnight',
                'interval': 1,
                'utc': True
            }
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': level,
        }
    }

    dictConfig(conf)

