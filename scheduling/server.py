from flask import Flask, request
import scheduling.db as database
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World\n'


@app.route('/finished', methods=['GET'])
def get_finished():
    if request.method == 'GET':
        db = database.Database('data.db')
        finished_departments = db.get_finished_departments()
        return str(finished_departments)


@app.route('/courses', methods=['GET'])
def get_courses():
    if request.method == 'GET':
        db = database.Database('data.db')
        data = db.get_courses()
        dict = []
        for x in data:
            n = {}
            n["department"] = x[0]
            n["course_number"] = x[1]
            dict.append(n)

        json_string = json.dumps(dict)
        return json_string


@app.route('/class', methods=['GET'])
def get_class():
    if request.method == 'GET':
        department = request.args.get('department')
        course_number = request.args.get('course_number')
        db = database.Database('courses.db')

        data = db.get_course_sections(course_number, department)
        dict = []
        for x in data:
            n = {}
            n["department"] = x[0]
            n["course_number"] = x[1]
            n["full_name"] = x[2]
            n["type"] = x[3]
            n["instructor"] = x[4]
            n["section_letter"] = x[5]
            n["section_number"] = x[6]
            n["start_time"] = x[7]
            n["end_time"] = x[8]
            n["facility"] = x[9]
            n["basis"] = x[10]
            n["units_min"] = x[11]
            n["units_max"] = x[12]
            n["mo"] = x[13]
            n["tu"] = x[14]
            n["we"] = x[15]
            n["th"] = x[16]
            n["fr"] = x[17]

            dict.append(n)

        json_string = json.dumps(dict)
        return json_string
