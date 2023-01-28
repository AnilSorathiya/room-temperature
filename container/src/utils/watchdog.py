import os
import sys
from dotenv import load_dotenv
from loguru import logger

load_dotenv(verbose=True)


class Watchdog:
    def __init__(self):
        level_debug = os.getenv("LOG_LEVEL")
        logger.opt(ansi=True)
        logger.opt(record=True)
        logger.add(sys.stderr, format="{time} {level} {message}", filter="RESTAPI", level=level_debug)

    @staticmethod
    def info(message):
        logger.level("INFO", no=10, color="<blue>", icon="🔷")
        logger.info(message)

    @staticmethod
    def debug(message):
        logger.level("DEBUG", no=38, color="<yellow>", icon="🔶")
        logger.debug(message)
