import sqlite3


DATABASE_NAME = "knowledge.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_user(name, email, password):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    """, (name, email, password))

    connection.commit()
    connection.close()


def get_user(email, password):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    connection.close()

    return user


def add_knowledge(title, category, content, author):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO knowledge
        (title, category, content, author)
        VALUES (?, ?, ?, ?)
    """, (title, category, content, author))

    connection.commit()
    connection.close()


def get_all_knowledge():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM knowledge
        ORDER BY id DESC
    """)

    knowledge = cursor.fetchall()

    connection.close()

    return knowledge


def search_knowledge(keyword):
    connection = get_connection()

    cursor = connection.cursor()

    search_text = f"%{keyword}%"

    cursor.execute("""
        SELECT * FROM knowledge
        WHERE title LIKE ?
        OR category LIKE ?
        OR content LIKE ?
        ORDER BY id DESC
    """, (search_text, search_text, search_text))

    results = cursor.fetchall()

    connection.close()

    return results