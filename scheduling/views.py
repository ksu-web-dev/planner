import json
import dataclasses
from typing import List, Dict, Any
from .section import Section


def render_schedule_list(schedules: List[List[Section]]) -> List[List[Dict]]:
    return list(map(render_schedule, schedules))


def render_schedule(sections: List[Section]) -> List[Dict]:
    return list(map(render_section, sections))


def render_section_list(sections: List[Section]) -> List[Dict]:
    return list(map(render_section, sections))


def render_section(section: Section) -> Dict:
    section_dict = dataclasses.asdict(section)
    return section_dict


