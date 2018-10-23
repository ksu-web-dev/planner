import sqlite3

conn = sqlite3.connect('courses.db')
c = conn.cursor()


def get_finished_departments():
    c.execute('select name from finished;')
    return c.fetchall()

def finish_department(name):
    c.execute('insert into finished values (?)', (name,))
    conn.commit()

def insert_course(course):
    pass
