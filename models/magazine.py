import sqlite3

def get_db_connection():
    conn = sqlite3.connect('magazine.db')
    return conn

class Magazine:
    _magazine_db = []

    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name  
        self._category = category  

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value
        if self._id is not None:
            self.update()  

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        if len(value) < 1:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value
        if self._id is not None:
            self.update()  

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()
        Magazine._magazine_db.append({'id': self._id, 'name': self._name, 'category': self._category})

    def update(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ?, category = ? WHERE id = ?', (self._name, self._category, self._id))
        conn.commit()
        conn.close()
        for magazine in Magazine._magazine_db:
            if magazine['id'] == self._id:
                magazine['name'] = self._name
                magazine['category'] = self._category
                break

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content
            FROM articles
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles ON articles.author_id = authors.id
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def __repr__(self):
        return f'<Magazine {self.name}>'
