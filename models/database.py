import sqlite3
from flask import g
import os

DATABASE = 'artisans.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create artisans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artisans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                craft_type TEXT,
                location TEXT,
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artisan_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artisan_id) REFERENCES artisans (id)
            )
        ''')
        # Create generated_content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artisan_id INTEGER NOT NULL,
                content_type TEXT NOT NULL,  -- 'text' or 'image'
                prompt TEXT,
                generated_text TEXT,
                generated_image_url TEXT,
                approval_status TEXT DEFAULT 'pending',
                include_quote INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artisan_id) REFERENCES artisans (id)
            )
        ''')
        conn.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid

def migrate_db():
    """Migrate the database schema by adding missing columns."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Add materials column to artisans table if not exists
        try:
            cursor.execute("ALTER TABLE artisans ADD COLUMN materials TEXT")
        except sqlite3.OperationalError:
            # Column already exists
            pass

        # Add approval_status and include_quote columns to generated_content table
        try:
            cursor.execute("ALTER TABLE generated_content ADD COLUMN approval_status TEXT DEFAULT 'pending'")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE generated_content ADD COLUMN include_quote INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass

        conn.commit()
