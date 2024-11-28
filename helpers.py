import sqlite3

def connect_db(language):
    db_name = f"poems_{language}.db"
    return sqlite3.connect(db_name)

def create_table(language):
    conn = connect_db(language)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date_added TEXT NOT NULL,
            language TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_poem(language, title, content, date_added):
    create_table(language)
    conn = connect_db(language)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO poems (title, content, date_added, language)
        VALUES (?, ?, ?, ?)
    ''', (title, content, date_added, language))
    conn.commit()
    conn.close()

def fetch_all_poems(language):
    create_table(language)  # Ensure the correct table is created
    conn = connect_db(language)
    cursor = conn.cursor()
    cursor.execute(f'SELECT id, title, content, date_added, language FROM {language}')  # Language-specific table
    poems = cursor.fetchall()
    print(f"Fetched poems for language '{language}': {poems}")  # Debugging line
    conn.close()
    return poems

def delete_poem_by_id(language, poem_id):
    conn = connect_db(language)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM poems WHERE id = ?', (poem_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()
    return affected_rows
