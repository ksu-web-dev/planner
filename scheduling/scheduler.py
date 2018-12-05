from .db import Database
from .section import Section
import itertools


class Scheduler():
    def __init__(self, db='data.db'):
        self.db = Database(db)

    def get_parsed_course_departments(self):
        departments = self.db.get_finished_departments()
        return list(map(lambda x: x[0], departments))

    def get_courses(self):
        courses = self.db.get_courses()
        return list(map(lambda x: {"department": x[0], "course_number": x[1]}, courses))

    def get_course_sections(self, department, course_number):
        sections_data = self.db.get_course_sections(department, course_number)
        return list(map(lambda x: Section(*x), sections_data))

    def schedule(self, courses):
        course_sections = []
        schedules = []

        for c in courses:
            department = c["department"]
            course_number = c["course_number"]

            sections = self.db.get_course_sections(department, course_number)
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
