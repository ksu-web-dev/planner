import sqlite3

conn = sqlite3.connect('courses.db')
c = conn.cursor()

c.execute('drop table if exists finished;')
c.execute('create table finished (name text);')

conn.commit()