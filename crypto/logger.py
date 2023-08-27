from logging.config import dictConfig


def build_logger_config():
    return {
        "version": 1,
        "root": {"handlers": ["console"], "level": "DEBUG"},
        "handlers": {"console": {"formatter": "std_out", "class": "logging.StreamHandler", "level": "DEBUG"}},
        "formatters": {
            "std_out": {
                "format": "%(asctime)s : %(levelname)s : %(module)s : %(message)s",
                "datefmt": "%d-%m-%Y %I:%M:%S",
            }
        },
    }


def configure_logging():
    dictConfig(build_logger_config())
