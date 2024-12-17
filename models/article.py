from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, title, author, magazine):
        if not isinstance(author, Author):
            raise Exception("author must be an instance of Author class")
        
        if not isinstance(magazine, Magazine):
            raise Exception("magazine must be an instance of Magazine class")
        
        if not isinstance(title, str):
            raise Exception("Article's title must be of type string")
        if not (5<= len(title) <=50):
            raise Exception("Article's titles must be between 5 and 50 characters, inclusive")
        
        self._title = title
        self._author = author
        self._magazine = magazine

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)"
        cursor.execute(sql, (self._title, self._author.id, self._magazine.id))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()


    def __repr__(self):
        return f'<Article {self._title}>'
    
    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT authors.id, authors.name 
            FROM authors 
            JOIN articles 
            ON authors.id = articles.author_id 
            WHERE articles.id = ? 
        """
        cursor.execute(sql, (self._id,))
        author_data = cursor.fetchone()
        conn.close()

        if author_data:
            return author_data
        else:
            return None
    
    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM magazines
            JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        """

        cursor.execute(sql, (self._id,))
        magazine_data = cursor.fetchone()
        conn.close()

        if magazine_data:
            return magazine_data
        else:
            return None
        
    def add_content(self, content):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "UPDATE articles SET content = ? WHERE id = ?"
        cursor.execute(sql, (content, self._id))
        conn.commit()

        conn.close()
        
        

