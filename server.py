from flask import Flask, request
import db as database

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World\n'


@app.route('/finished', methods=['GET'])
def get_finished():
    if request.method == 'GET':
        db = database.Database('courses.db')
        return str(db.get_finished_departments())
