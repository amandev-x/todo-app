
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        # Use Replit's PostgreSQL environment variables
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            # Fallback connection for development
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                database=os.environ.get('DB_NAME', 'todoapp'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', 'password'),
                port=os.environ.get('DB_PORT', '5432')
            )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    task TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Database initialization error: {e}")

@app.route('/')
def index():
    conn = get_db_connection()
    todos = []
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM todos ORDER BY created_at DESC')
            todos = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching todos: {e}")
    
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO todos (task) VALUES (%s)', (task,))
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Error adding todo: {e}")
    
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE todos SET completed = NOT completed WHERE id = %s', (todo_id,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error updating todo: {e}")
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error deleting todo: {e}")
    
    return redirect(url_for('index'))

@app.route('/api/todos')
def api_todos():
    conn = get_db_connection()
    todos = []
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM todos ORDER BY created_at DESC')
            todos = [dict(todo) for todo in cur.fetchall()]
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching todos: {e}")
    
    return jsonify(todos)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)