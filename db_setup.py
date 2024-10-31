import psycopg2
from config import DATABASE


def create_tables():
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS student_management (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS teacher_management (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        subject VARCHAR(100)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS student_teacher (
        student_id INT REFERENCES student_management(id) ON DELETE CASCADE,
        teacher_id INT REFERENCES teacher_management(id) ON DELETE CASCADE,
        PRIMARY KEY (student_id, teacher_id)
    );
    ''')

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
