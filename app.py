from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'students.db'

# Initialize DB if not exists
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )''')
        conn.commit()
        conn.close()

init_db()

# Home page: display all students
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)', (name, email, course))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        c.execute('UPDATE students SET name=?, email=?, course=? WHERE id=?', (name, email, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute('SELECT * FROM students WHERE id=?', (id,))
        student = c.fetchone()
        conn.close()
        return render_template('edit_student.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)