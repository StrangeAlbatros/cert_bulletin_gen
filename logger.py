#!/usr/bin/python3
# -*- coding: utf-8 -*-

from logging import Logger, Formatter, StreamHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL

class ColoredFormatter(Formatter):
    """ Formatter with color """
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GREY = range(30, 39)
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[0;%dm"
    BOLD_SEQ = "\033[1m"
    MESSAGE = "%(asctime)s %(message)s "

    FORMAT = {
        DEBUG: CYAN,
        INFO: WHITE,
        WARNING: YELLOW,
        ERROR: RED,
        CRITICAL: RED,
    }

    def format(self, record):
        """ Definition of the log format """
        log_fmt = self.COLOR_SEQ % self.FORMAT.get(record.levelno)
        log_fmt += self.MESSAGE
        log_fmt += self.RESET_SEQ
        formatter = Formatter(log_fmt)
        return formatter.format(record)

class CustomLogger(Logger):
    """ Custom logger """
    def __init__(self, name: str) -> None:
        super().__init__(name, INFO)
        handler = StreamHandler()
        handler.setFormatter(ColoredFormatter())
        self.addHandler(handler)

    def set_debug(self):
        """ Activate debug mode """
        self.setLevel(DEBUG)

LOGGER = CustomLogger("Logger")