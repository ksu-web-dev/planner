from dataclasses import dataclass

@dataclass
class Section:
    section_letter: str = ''
    type: str = ''
    units: str = ''
    basis: str = ''
    facility: str = ''
    start_time: str = ''
    end_time: str = ''
    instructor: str = ''
    full_name: str = ''
    section_number: str = ''
    course_number: int = 0
    department: str = ''
    mo: bool = False
    tu: bool = False
    we: bool = False
    th: bool = False
    fr: bool = False
