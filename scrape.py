import requests
from bs4 import BeautifulSoup
import datetime
import logging
from db import Database
import re
import time
import dataclasses

from section import Section

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)


def main():
    start_crawl()


def start_crawl():
    db = Database('data.db')
    finished_departments = db.get_finished_departments()
    all_departments = fetch_departments()

    for department in parse_departments(all_departments):
        if (department,) in (finished_departments):
            continue

        page = fetch_courses(department)

        for course in parse_courses(page):
            course_data = dataclasses.astuple(course)
            logger.debug(course_data)
            db.insert_course(course_data)

        db.finish_department(department)
        time.sleep(1)


def fetch_departments():
    url = 'https://courses.k-state.edu/spring2019/schedule.html'
    logger.info(f'Fetching departments page: {url}')
    r = requests.get(url)
    return r.text


def fetch_courses(department):
    url = f'https://courses.k-state.edu/spring2019/{department}'
    logger.info(f'Fetching courses page: {url}')
    r = requests.get(url)
    return r.text


def parse_departments(page):
    logger.info('Parsing list of departments')
    soup = BeautifulSoup(page, 'html.parser')

    for a in soup.select('.ksu-main-content li > a'):
        department = a['href'][:-1]
        logger.debug(f'Parsed department: {department}')

        yield department


def parse_courses(page):
    soup = BeautifulSoup(page, 'html.parser')

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
            instructor=tbody.select_one(f'.st td:nth-of-type(9)').get_text(),
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
        parsed_units = tbody.select_one(f'.st td:nth-of-type(4)').get_text(),

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
            section.mo = True
        if 'T' in days:
            section.tu = True
        if 'W' in days:
            section.we = True
        if 'U' in days:
            section.th = True
        if 'F' in days:
            section.fr = True

        # Parse the times
        parsed_hours = tbody.select_one(f'.st td:nth-of-type(7)').get_text()
        hours = re.findall('[0-9]+:[0-9]+', parsed_hours)

        if len(hours) > 1:
            section.start_time = hours[0]
            section.end_time = hours[1]
            cycle = re.findall('a.m.|p.m.', parsed_hours)

            if len(cycle) > 1 or hours[0] == 'p.m.':
                hour = int(re.search('(.*):', hours[1])[1])
                minutes = re.search(':(.*)', hours[1])[1]

                if hour > 12:
                    section.endtime = f'{hour + 12}:{minutes}'

        # Parse some edge cases
        if section.facility == 'books':
            section.facility = tbody.select_one(
                f'.st td:nth-of-type(10)').get_text()

        if section.instructor == 'books':
            section.instructor = tbody.select_one(
                f'.st td:nth-of-type(10)').get_text()

        logger.debug(section)
        yield section


if __name__ == "__main__":
    main()
