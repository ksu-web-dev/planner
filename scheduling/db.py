import sqlite3


class Database():
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    def get_course_sections(self, course_number, department):
        self.c.execute(
            "select * from sections where course_number = (?) and department = (?)", (course_number, department))
        return self.c.fetchall()

    def get_courses(self):
        self.c.execute('select department, course_number from sections;')
        return self.c.fetchall()

    def get_finished_departments(self):
        self.c.execute('select name from finished;')
        return self.c.fetchall()

    def finish_department(self, name):
        self.c.execute('insert into finished values (?)', (name,))
        self.conn.commit()

    def get_sections(self):
        self.c.execute('select * from sections')
        return self.c.fetchall()

    def insert_section(self, course):
        self.c.execute("""
        insert into sections (
            department,
            course_number,
            full_name,
            type,
            instructor,
            section_letter,
            section_number,
            start_time,
            end_time,
            facility,
            basis,
            units_min,
            units_max,
            mo,
            tu,
            we,
            th,
            fr
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, course)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
