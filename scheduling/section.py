from dataclasses import dataclass

@dataclass
class Section:
    department: str = ''
    course_number: int = 0
    full_name: str = ''
    type: str = ''
    instructor: str = ''
    section_letter: str = ''
    section_number: int = 0
    start_time: str = ''
    end_time: str = ''
    facility: str = ''
    basis: str = ''
    units_min: int = 0
    units_max: int = 0
    mo: bool = False
    tu: bool = False
    we: bool = False
    th: bool = False
    fr: bool = False
