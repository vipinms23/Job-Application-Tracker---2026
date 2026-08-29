import sqlite3

DB_FILE = 'jobs.db'

def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    # Configure to return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the applications table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Company TEXT,
            Role TEXT,
            Salary TEXT,
            stage TEXT,
            applied_on TEXT,
            link TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_application(company, role, salary, stage, applied_on, link):
    """Add a new job application to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (Company, Role, Salary, stage, applied_on, link)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (company, role, salary, stage, applied_on, link))
    conn.commit()
    conn.close()

def get_all_applications():
    """Retrieve all job applications from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_application_stage(app_id, new_stage):
    """Update the stage of a specific job application."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE applications
        SET stage = ?
        WHERE ID = ?
    ''', (new_stage, app_id))
    conn.commit()
    conn.close()

def delete_application(app_id):
    """Delete a job application from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM applications WHERE ID = ?', (app_id,))
    conn.commit()
    conn.close()
