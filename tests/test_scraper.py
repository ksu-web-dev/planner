import unittest
from scheduling import Scraper
import datetime


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.s = Scraper()

    def test_parse_courses(self):
        page = ''

        with open('tests/courses.html', 'r') as f:
            page = f.read()

        sections = [x for x in self.s.parse_courses(page)]

        self.assertEqual(len(sections), 71)
        self.assertEqual(sections[0].department, 'ECON')
        self.assertEqual(sections[0].full_name, 'Principles Of Macroeconomics')
        self.assertEqual(sections[0].days, int('10101', 2))
        self.assertEqual(sections[0].start_time, datetime.time(8, 30))
        self.assertEqual(sections[0].end_time, datetime.time(9, 20))
        self.assertEqual(sections[0].facility, 'WA 231')
        self.assertEqual(sections[0].instructor, 'Al-Hamdi, Mohaned Talib')

    def test_convert_to_time(self):
        t = self.s.convert_to_time('12:30')
        self.assertEqual(t, datetime.time(12, 30))
        t = self.s.convert_to_time('12:30', True)
        self.assertEqual(t, datetime.time(12, 30))
        t = self.s.convert_to_time('1:30', True)
        self.assertEqual(t, datetime.time(13, 30))
        t = self.s.convert_to_time('10:30')
        self.assertEqual(t, datetime.time(10, 30))

    def test_parse_times(self):
        am_pm = '11:30 a.m. - 12:45 p.m.'
        am = '9:30 - 10:45 a.m.'
        pm = '12:30 - 1:20 p.m.'

        self.assertEqual(self.s.parse_times(am_pm),
                         (datetime.time(11, 30), datetime.time(12, 45)))

        self.assertEqual(self.s.parse_times(am),
                         (datetime.time(9, 30), datetime.time(10, 45)))

        self.assertEqual(self.s.parse_times(pm),
                         (datetime.time(12, 30), datetime.time(13, 20)))
