import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },

    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'loggs/loggs.txt',
            'formatter': 'default_formatter',
        }
    },

    'loggers': {
        'middlewares': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
