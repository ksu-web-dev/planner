from flask import Flask, request, jsonify
import planner.db as database
from planner.scheduler import Scheduler
import planner.views as views
from planner.section import Section
from functools import wraps
import json
import time

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World\n'


@app.route('/courses', methods=['GET'])
def get_courses():
    s = Scheduler()
    courses = s.get_courses()
    return jsonify(courses)


@app.route('/courses/parsed', methods=['GET'])
def get_finished():
    s = Scheduler()
    response = s.get_parsed_course_departments()
    return jsonify(response)


@app.route('/courses/<department>/<course_number>/sections', methods=['GET'])
def get_course_sections(department, course_number):
    s = Scheduler()
    sections = s.get_course_sections(department, course_number)
    response = views.render_section_list(sections)
    return jsonify(response)


@app.route('/schedules', methods=['POST'])
def get_schedule():
    s = Scheduler()
    data = request.get_json()
    schedules = s.schedule(data)
    response = views.render_schedule_list(schedules)
    return jsonify(response)
