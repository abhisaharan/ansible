# The logger manager class can be imported and used anywhere for logging functionalities and debugging.

import time
import os
import ConfigParser
import logging
from logging.handlers import RotatingFileHandler
import __builtin__

_max_log_bytes = 1073741824
#5*1024*1024
_cache = {}


def _init_logger(name):
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_formatter = logging.Formatter(format)
    log_file = "%s.log" % name
    _handler = RotatingFileHandler(log_file, mode='a', maxBytes=_max_log_bytes,
            backupCount=5, delay=0)
    _handler.setFormatter(log_formatter)
    _handler.setLevel(logging.DEBUG)
    return _handler


def get_app_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_init_logger(name))
    return logger


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(
                    Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerManager(object):
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def getLogger(name=None):
        if not name:
            return get_app_logger(__name__)
        elif name not in LoggerManager._loggers.keys():
            LoggerManager._loggers[name] = get_app_logger(name)
        return LoggerManager._loggers[name]


class ScriptEnvironment:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        module_path = __file__.split("/")
        self.config.readfp(
                open("/".join(module_path[0:-1]) + '/config/defaults.conf'))
        self.config.read([os.path.expanduser('~/.custom.conf')])


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def cache(function, arg):
    from functools import wraps
    duration = arg
    @wraps(function)
    def wrapper(*args, **kwargs):
# Note: enable only during debugging
#        if hasattr(__builtin__, "_ist_utils_logname"):
#            logfilename = __builtin__._ist_utils_logname
#        else:
#            logfilename = __name__
#        logger = LoggerManager.getLogger(logfilename)
        key = function.__name__
        get_cached = False
        # This handles only class methods for now
        if args and args[1] != None:
            key = key + "_" + str(args[1])
        if key in _cache:
            elapsed = time.time() - _cache[key][0]
#            logger.debug("key: %r elapsed: %r duration: %r",
#                    key, elapsed, duration)
            if int(elapsed) < duration:
                get_cached = True
#        logger.debug("Cache size: %r", len(_cache.keys()))
        if get_cached:
#            logger.debug("Get cached item: %r", key)
            return _cache[key][1]
        else:
            rv = function(*args)
            try:
                del _cache[key]
            except KeyError:
                pass
#            logger.debug("Caching item: %r", key)
            _cache[key] = (time.time(), rv)
            return rv
    return wrapper