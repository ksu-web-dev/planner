import sqlite3
import logging
from flask import Flask
import os


class Database():
    def __init__(self, db):
        self.db = db
        app = Flask(__name__)
        self.conn = sqlite3.connect(os.path.join(app.root_path, self.db))
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)

    def insert_query(self, table, params):
        fields = ','.join(params)
        values = '?,' * len(params)
        query = f'insert into {table} ({fields}) values ({values[:-1]})'
        return query

    def get_course_sections(self, department, course_number):
        self.c.execute(
            "select * from sections where course_number = (?) and department = (?)", (course_number, department))
        sections = self.c.fetchall()
        self.logger.debug(f'Section data: {sections}')
        return sections

    def get_courses(self):
        self.c.execute('select department, course_number from sections;')
        return self.c.fetchall()

    def get_finished_departments(self):
        self.c.execute('select name from finished;')
        departments = self.c.fetchall()
        self.logger.debug(f'Finished departments data: {departments}')
        return departments

    def finish_department(self, name):
        self.c.execute('insert into finished values (?)', (name,))
        self.conn.commit()

    def insert_section(self, course):
        fields = ['department', 'course_number', 'full_name', 'type', 'instructor', 'section_letter',
                  'section_number', 'start_time', 'end_time', 'facility', 'basis', 'units_min', 'units_max', 'days']
        query = self.insert_query('sections', fields)
        self.c.execute(query, course)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
