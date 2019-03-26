import re
import datetime
import requests
import logging
import time
from bs4 import BeautifulSoup
from scheduling import Database
from scheduling import Section


class Scraper:
    def __init__(self, db='data.db'):
        self.db = Database(db)
        self.logger = logging.getLogger(__name__)

    def scrape(self):
        finished_departments = self.db.get_finished_departments()
        all_departments = self.fetch_departments()

        for department in self.parse_departments(all_departments):
            if (department,) in (finished_departments):
                continue

            page = self.fetch_courses(department)

            for course in self.parse_courses(page):
                course_data = course.to_tuple()
                self.logger.debug(course_data)
                self.db.insert_section(course_data)

            self.db.finish_department(department)
            time.sleep(1)
            break

    def fetch_departments(self):
        url = 'https://courses.k-state.edu/spring2019/schedule.html'
        self.logger.info(f'Fetching departments page: {url}')
        r = requests.get(url)
        return r.text

    def fetch_courses(self, department):
        url = f'https://courses.k-state.edu/spring2019/{department}'
        self.logger.info(f'Fetching courses page: {url}')
        r = requests.get(url)
        return r.text

    def parse_departments(self, page):
        self.logger.info('Parsing list of departments')
        soup = BeautifulSoup(page, 'html.parser')

        for a in soup.select('.ksu-main-content li > a'):
            department = a['href'][:-1]
            self.logger.debug(f'Parsed department: {department}')

            yield department

    def parse_courses(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        self.logger.info('Parsing sections from course page')

        for tbody in soup.select('.section'):
            # Parse the easier values from the page
            section = Section(
                section_letter=tbody.select_one(
                    f'.st td:nth-of-type(1)').get_text(),
                type=tbody.select_one(f'.st td:nth-of-type(2)').get_text(),
                section_number=tbody.select_one(
                    f'.st td:nth-of-type(3)').get_text(),
                basis=tbody.select_one(f'.st td:nth-of-type(5)').get_text(),
                facility=tbody.select_one(f'.st td:nth-of-type(8)').get_text(),
                instructor=tbody.select_one(
                    f'.st td:nth-of-type(9)').get_text(),
            )

            # Parse the course department, name and number
            course_tbody = tbody.findPreviousSibling()
            while course_tbody['class'][0] != 'course-header':
                course_tbody = course_tbody.findPreviousSibling()

            department_and_number = course_tbody.select_one(
                'span.number').get_text()

            section.department = re.search(
                r'([A-Z]*)', department_and_number)[1]
            section.course_number = re.search(
                r'[A-Z]*(.*)', department_and_number)[1]
            section.full_name = course_tbody.select('.name')[0].get_text()

            # Parse the number of units
            parsed_units = tbody.select_one(
                f'.st td:nth-of-type(4)').get_text(),

            if (len(parsed_units) == 1):
                section.units_min = parsed_units[0]
                section.units_max = parsed_units[0]
            else:
                units = re.search(r'([0-9]*)-([0-9]*)', parsed_units)
                section.units_min = units[1]
                section.units_max = units[2]

            # Parse the days
            parsed_days = tbody.select_one(f'.st td:nth-of-type(6)').get_text()
            days = re.findall('[A-Z]+', parsed_days)

            if 'M' in days:
                section.days |= int('10000', 2)
            if 'T' in days:
                section.days |= int('01000', 2)
            if 'W' in days:
                section.days |= int('00100', 2)
            if 'U' in days:
                section.days |= int('00010', 2)
            if 'F' in days:
                section.days |= int('00001', 2)

            # Parse the times
            times = tbody.select_one(
                f'.st td:nth-of-type(7)').get_text()

            if len(times) > 1 and times != 'books':
                (start_time, end_time) = self.parse_times(times)
                section.start_time = start_time
                section.end_time = end_time

            # Parse some edge cases
            if section.facility == 'books':
                section.facility = tbody.select_one(
                    f'.st td:nth-of-type(10)').get_text()

            if section.instructor == 'books':
                section.instructor = tbody.select_one(
                    f'.st td:nth-of-type(10)').get_text()

            self.logger.debug(section)
            yield section

    def parse_times(self, time):
        hours = re.findall('[0-9]+:[0-9]+', time)

        am_pm = re.match('.*a.m.*p.m.', time)
        both_pm = re.match('.*-.*p.m.', time)

        convert_start_time = False
        convert_end_time = False

        if am_pm:
            convert_end_time = True
        elif both_pm:
            convert_start_time = True
            convert_end_time = True

        start_time = self.convert_to_time(hours[0], convert_start_time)
        end_time = self.convert_to_time(hours[1], convert_end_time)
        return (start_time, end_time)

    def convert_to_time(self, time_str, pm=False):
        times = re.search('(.*):(.*)', time_str)
        hour = int(times[1])
        minutes = int(times[2])

        if hour < 12 and pm:
            hour += 12

        return datetime.time(hour, minutes)
