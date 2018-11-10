import unittest
from scheduling import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.s = Scheduler()

    def test_schedule(self):
        schedules = self.s.schedule([{"department": "ART", "course_number": 210}, {
            "department": "GEOL", "course_number": 102}])
