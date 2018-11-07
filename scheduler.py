from db import Database
from section import Section


class Scheduler():
    def __init__(self):
        self.db = Database('courses.db')

    def schedule(self):
        self.db = Database('data.db')
        sections = self.db.get_sections()
        sections = list(map(lambda s : Section(*s), sections))

        # Scheduling algorithm goes here