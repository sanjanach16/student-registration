from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'students'
}

# Establishing connection with MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Creating students table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        name VARCHAR(255) NOT NULL,
        student_id VARCHAR(10) PRIMARY KEY,
        year INT NOT NULL
    )
""")
conn.commit()

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/home')
def home():
    # Fetching all students' details from the database
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('home.html', students=students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        year = request.form['year']

        # Inserting new student details into the database
        cursor.execute("INSERT INTO students (name, student_id, year) VALUES (%s, %s, %s)", (name, student_id, year))
        conn.commit()

        return redirect(url_for('home'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
