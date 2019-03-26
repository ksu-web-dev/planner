import logging.config
from .section import Section
from .db import Database
from .scheduler import Scheduler
from .scraper import Scraper
import os
from flask import Flask

app = Flask(__name__)
logging.config.fileConfig(os.path.join(app.root_path, 'logging.ini'))
