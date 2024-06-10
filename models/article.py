import sqlite3

def get_db_connection():
    return sqlite3.connect('magazine.db')

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) < 5 or len(value) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = value

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self._author_id,))
        author_data = cursor.fetchone()
        conn.close()
        if author_data:
            return Author(author_data[0], author_data[1]) 
        else:
            return None

    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self._magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()
        if magazine_data:
            return Magazine(magazine_data[0], magazine_data[1], magazine_data[2])  
        else:
            return None

    def _save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (self._title, self._content, self._author_id, self._magazine_id))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def __repr__(self):
        return f'<Article {self.title}>'
