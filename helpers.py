import sqlite3

def connect_db(language):
    """Establish a connection to the database."""
    db_name = f"poems_{language}.db"
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(language):
    """Create the poems table if it doesn't exist."""
    conn = connect_db(language)
    if conn is None:
        return
    try:
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
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def insert_poem(language, title, content, date_added):
    """Insert a new poem into the database."""
    create_table(language)  # Ensure the table is created
    conn = connect_db(language)
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO poems (title, content, date_added, language)
            VALUES (?, ?, ?, ?)
        ''', (title, content, date_added, language))
        conn.commit()
        print(f"Poem '{title}' added to {language} database successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting poem: {e}")
    finally:
        conn.close()

def fetch_all_poems(language):
    """Fetch all poems for a specific language."""
    create_table(language)  # Ensure the correct table is created
    conn = connect_db(language)
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, title, content, date_added, language FROM poems')
        poems = cursor.fetchall()
        print(f"Fetched poems: {poems}")
        return poems
    except sqlite3.Error as e:
        print(f"Error fetching poems: {e}")
        return []
    finally:
        conn.close()

def recreate_table_preserve_order(language):
    """Recreate the poems table with reordered IDs, preserving the order by date_added."""
    conn = connect_db(language)
    if conn is None:
        return
    try:
        cursor = conn.cursor()

        # Step 1: Create a temporary table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS poems_temp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date_added TEXT NOT NULL,
            language TEXT NOT NULL
        )
        """)

        # Step 2: Copy data from the original table, ordering by date_added
        cursor.execute("""
        INSERT INTO poems_temp (title, content, date_added, language)
        SELECT title, content, date_added, language
        FROM poems
        ORDER BY date_added
        """)

        # Step 3: Drop the old table
        cursor.execute("DROP TABLE poems")

        # Step 4: Rename the temporary table to the original name
        cursor.execute("ALTER TABLE poems_temp RENAME TO poems")

        # Commit changes
        conn.commit()
        print(f"Table for language '{language}' recreated successfully with reordered IDs.")
    except sqlite3.Error as e:
        print(f"Error during table recreation: {e}")
    finally:
        conn.close()

def delete_poem_by_id(language, poem_id):
    """Delete a poem by its ID and reorder the table to maintain sequential IDs."""
    conn = connect_db(language)
    if conn is None:
        return 0
    try:
        cursor = conn.cursor()
        # Delete the poem
        cursor.execute('DELETE FROM poems WHERE id = ?', (poem_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        
        if affected_rows > 0:
            print(f"Poem with ID {poem_id} deleted successfully.")
            # Reorder IDs after deletion
            recreate_table_preserve_order(language)
        else:
            print(f"No poem found with ID {poem_id}.")
        return affected_rows
    except sqlite3.Error as e:
        print(f"Error deleting poem: {e}")
        return 0
    finally:
        conn.close()
        
