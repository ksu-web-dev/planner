import sqlite3

class Database():
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    def get_finished_departments(self):
        self.c.execute('select name from finished;')
        return self.c.fetchall()

    def finish_department(self, name):
        self.c.execute('insert into finished values (?)', (name,))
        self.conn.commit()

    def insert_course(self, course):
        pass

    def __del__(self):
        self.conn.close()
