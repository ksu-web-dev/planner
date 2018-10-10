import requests
from bs4 import BeautifulSoup
import datetime


def main():
    pass


def get_page():
    url = 'https://courses.k-state.edu/spring2019/AR/'
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def parse_page(soup):
    for course in soup.select('.course-header'):
        section = course.findNextSibling()

        course_name = course.select_one('.name').get_text()
        course_number = course.select_one('.number').get_text()

        while(section is not None and section['class'][0] == 'section'):
            section_letter = parse_section_column(section, 1)
            section_type = parse_section_column(section, 2)
            section_number = parse_section_column(section, 3)
            units = parse_section_column(section, 4)
            basis = parse_section_column(section, 5)
            days = parse_section_column(section, 6)
            hours = parse_section_column(section, 7)
            facility = parse_section_column(section, 8)
            instructor = parse_section_column(section, 9)

            if (instructor == 'books'):
                instructor = parse_section_column(section, 10)

            print(f'{course_number} {course_name}')
            section = section.findNextSibling()


def parse_section_column(section, index):
    return section.select_one(f'.st td:nth-of-type({index})').get_text()


if __name__ == "__main__":
    main()
