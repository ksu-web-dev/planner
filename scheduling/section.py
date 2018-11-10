import dataclasses
import time


@dataclasses.dataclass
class Section:
    department: str = ''
    course_number: int = 0
    full_name: str = ''
    type: str = ''
    instructor: str = ''
    section_letter: str = ''
    section_number: int = 0
    start_time: time.time = None
    end_time: time.time = None
    facility: str = ''
    basis: str = ''
    units_min: int = 0
    units_max: int = 0
    days: int = 0

    def __post_init__(self):
        if self.start_time is str:
            self.start_time = time.strptime(self.start_time, "%H:%M")

        if self.end_time is str:
            self.end_time = time.strptime(self.end_time, "%H:%M")

    def to_tuple(self):
        data = dataclasses.asdict(self)

        if self.start_time:
            data['start_time'] = self.start_time.strftime("%H:%M")

        if self.end_time:
            data['end_time'] = self.end_time.strftime("%H:%M")

        return tuple(data.values())
