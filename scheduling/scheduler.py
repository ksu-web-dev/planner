from .db import Database
from .section import Section
import itertools


class Scheduler():
    def __init__(self, db='data.db'):
        self.db = Database(db)

    def schedule(self, courses):
        course_sections = []
        schedules = []

        for c in courses:
            course_number = c["course_number"]
            department = c["department"]

            sections = self.db.get_course_sections(course_number, department)
            sections = [s for s in (map(lambda x: Section(*x), sections))]

            course_sections.append(sections)

        combinations = [x for x in itertools.product(*course_sections)]

        def valid_sections(sections):
            for section in sections:
                if section.start_time == None or section.end_time == None:
                    continue

                for other_section in sections:
                    if other_section.start_time == None or other_section.end_time == None:
                        continue

                    if section.days & other_section.days != 0:
                        if other_section.start_time < section.start_time < other_section.end_time:
                            return False

                        if other_section.start_time < section.end_time < other_section.end_time:
                            return False

            return True

        schedules = [x for x in filter(valid_sections, combinations)]
        return schedules
