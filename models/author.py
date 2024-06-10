import sqlite3

def get_db_connection():
    conn = sqlite3.connect('magazine.db')
    return conn

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name, str):
            raise TypeError("name must be of type str")
        if len(name) == 0:
            raise ValueError("name must be longer than 0 characters")
        self._name = name
        self._id = id
        if id is None:
            self._save_to_db()

    def _save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __setattr__(self, name, value):
        if name == "_name" and hasattr(self, "_name"):
            raise AttributeError("name attribute is immutable")
        super().__setattr__(name, value)

    def __repr__(self):
        return f'<Author {self.name}>'

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles ON articles.magazine_id = magazines.id
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines
