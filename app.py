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

    try:
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

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

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
    try:
        cur.execute(
            "INSERT INTO student_management (name, age) VALUES (%s, %s) RETURNING id;", (name, age))
        student_id = cur.fetchone()[0]
        conn.commit()

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({'id': student_id, 'message': 'Student added successfully'})


@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        data = request.get_json()
        name = data['name']
        age = data['age']
        cur.execute("UPDATE student_management SET name = %s, age = %s WHERE id = %s;",
                    (name, age, student_id))
        conn.commit()

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500
    cur.close()
    conn.close()
    return jsonify({'message': 'Student updated successfully'})


@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "DELETE FROM student_management WHERE id = %s;", (student_id,))
        conn.commit()

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({'message': 'Student deleted successfully'})


@app.route('/student/<int:student_id>/teachers', methods=['GET'])
def get_teachers(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('''
            SELECT t.id, t.name, t.subject
            FROM teacher_management t
            JOIN student_teacher st ON t.id = st.teacher_id
            WHERE st.student_id = %s;
        ''', (student_id,))
        teachers = cur.fetchall()

        teacher_list = []
        for teacher in teachers:
            teacher_dict = {
                'id': teacher[0],
                'name': teacher[1],
                'subject': teacher[2]
            }
            teacher_list.append(teacher_dict)

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({'teachers': teacher_list})


# ========================================================================================


@app.route('/teacher', methods=['GET'])
def view_teachers():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM teacher_management;")

        teachers = cur.fetchall()

        teacher_list = []
        for teacher in teachers:
            teacher_dict = {
                'id': teacher[0],
                'name': teacher[1],
                'subject': teacher[2]
            }
            teacher_list.append(teacher_dict)

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()

    return jsonify(teacher_list)


@app.route('/teacher', methods=['POST'])
def create_teacher():
    data = request.get_json()

    name = data.get('name')
    subject = data.get('subject')

    if not name or not subject:
        return jsonify({'error': 'Name and subject are required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO teacher_management (name, subject) VALUES (%s, %s) RETURNING id;", (name, subject))
        teacher_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()

    return jsonify({'id': teacher_id, 'message': 'Teacher created successfully'}), 201


@app.route('/teacher/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    data = request.get_json()
    name = data['name']
    subject = data['subject']

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE teacher_management SET name = %s, subject = %s WHERE id = %s;",
                    (name, subject, teacher_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({'message': 'Teacher updated successfully'})


@app.route('/teacher/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM teacher_management WHERE id = %s;", (teacher_id,))
        conn.commit()

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({'message': 'Teacher deleted successfully'})


@app.route('/teacher/<int:teacher_id>/students', methods=['GET'])
def get_students_by_teacher(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('''
            SELECT s.id, s.name, s.age
            FROM student_management s
            JOIN student_teacher st ON s.id = st.student_id
            WHERE st.teacher_id = %s;
        ''', (teacher_id,))

        students = cur.fetchall()

        student_list = []
        for student in students:
            student_dict = {
                'id': student[0],
                'name': student[1],
                'age': student[2]
            }
            student_list.append(student_dict)

    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()

    return jsonify(student_list)


# ==========================================================================================================

# Mapp a student with a teacher
@app.route('/student/<int:student_id>/connect/<int:teacher_id>', methods=['POST'])
def connect_student_teacher(student_id, teacher_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM student_management WHERE id = %s;",
                (student_id,))
    student = cur.fetchone()

    cur.execute("SELECT id FROM teacher_management WHERE id = %s;",
                (teacher_id,))
    teacher = cur.fetchone()

    if not student:
        cur.close()
        conn.close()
        return jsonify({'error': 'Student not found'}), 404

    if not teacher:
        cur.close()
        conn.close()
        return jsonify({'error': 'Teacher not found'}), 404

    try:
        cur.execute(
            "INSERT INTO student_teacher (student_id, teacher_id) VALUES (%s, %s);", (student_id, teacher_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({'message': 'Student connected to teacher successfully'})


if __name__ == '__main__':
    app.run(debug=True)


# Mapp a teacher with multiple students in the list of studentIds
@app.route('/teacher/<int:teacher_id>/connect', methods=['POST'])
def connect_teacher_with_students(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the teacher exists
    cur.execute("SELECT id FROM teacher_management WHERE id = %s;",
                (teacher_id,))
    teacher = cur.fetchone()

    if not teacher:
        cur.close()
        conn.close()
        return jsonify({'error': 'Teacher not found'}), 404

    # Get list of studentIds
    data = request.get_json()
    student_ids = data.get('student_ids', [])

    if not isinstance(student_ids, list):
        cur.close()
        conn.close()
        return jsonify({'error': 'student_ids must be a list'}), 400

    successful_connections = []
    errors = []

    for student_id in student_ids:
        cur.execute(
            "SELECT id FROM student_management WHERE id = %s;", (student_id,))
        student = cur.fetchone()

        if not student:
            errors.append({'student_id': student_id,
                          'error': 'Student not found'})
            continue

        try:
            cur.execute(
                "INSERT INTO student_teacher (student_id, teacher_id) VALUES (%s, %s);", (student_id, teacher_id))
            successful_connections.append(student_id)
        except Exception as e:
            conn.rollback()
            errors.append({'student_id': student_id, 'error': str(e)})

    conn.commit()
    cur.close()
    conn.close()

    response = {
        'message': 'Connections processed',
        'successful_connections': successful_connections,
        'errors': errors
    }
    return jsonify(response)
