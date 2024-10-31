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

    student_list = []
    for student in students:
        student_dict = {
            'id': student[0],
            'name': student[1],
            'age': student[2]
        }
        student_list.append(student_dict)

    cur.close()
    conn.close()

    return jsonify(student_list)


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


@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    name = data['name']
    age = data['age']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE student_management SET name = %s, age = %s WHERE id = %s;",
                (name, age, student_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Student updated successfully'})


@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student_management WHERE id = %s;", (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Student deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
