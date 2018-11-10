import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('drop table if exists finished;')
c.execute('create table finished (name text);')

c.execute('drop table if exists sections;')
c.execute("""
create table sections (
    department text,
    course_number text,
    full_name text,
    type text,
    instructor text,
    section_letter text,
    section_number int,
    start_time text,
    end_time text,
    facility text,
    basis text,
    units_min integer,
    units_max integer,
    days integer
)
""")

conn.commit()
