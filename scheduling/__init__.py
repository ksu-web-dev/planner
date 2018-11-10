import logging.config
from .section import Section
from .db import Database
from .scheduler import Scheduler
from .scraper import Scraper

logging.config.fileConfig('logging.ini')