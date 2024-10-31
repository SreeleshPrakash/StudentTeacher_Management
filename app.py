# app.py
from flask import Flask, jsonify, request
import psycopg2
from config import DATABASE

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(**DATABASE)


@app.route('/student', methods=['GET'])
def view_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student_management;")
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(students)


@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data['name']
    age = data['age']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO student_management (name, age) VALUES (%s, %s) RETURNING id;", (name, age))
    student_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': student_id, 'message': 'Student added successfully'})


if __name__ == '__main__':
    app.run(debug=True)
