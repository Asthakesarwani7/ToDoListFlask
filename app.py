from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

#connect to SQLite DB
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#create tasj table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TEXT
                 )
                 ''')
    conn.commit()
    conn.close()
    print("Database initialized.")

#home route
@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

#add a new task
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    if title:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (title, created_at) VALUES (?, ?)',
                     (title, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
    return redirect('/')

#delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')




if __name__ == "__main__":
    print("Flask app is starting...")
    init_db()
    app.run(debug = True)  #to refresh automatically
    