from database.connection import get_db_connection
from models.author import Author




class Magazine:
    def __init__(self, id = None, name = None, category = None):
        if not isinstance(name, str):
            raise Exception("Magazine's name should be a string.")
        if not (2<= len(name) <=16):
            raise Exception("Magazine's name must be between 2 and 16 characters, inclusive.")
        
        if not isinstance(category, str):
            raise Exception("Magazine's category should be a string.")
        if len(category) == 0:
            raise Exception("Magazine category must be longer than 0 characters")
        self._name = name
        self._category = category
        self._id = id

        if id is None:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO magazines (name, category) VALUES (?, ?)"

            cursor.execute(sql, (name, category))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()


    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise Exception("Magazine's name should be a string.")
        if not (2<= len(new_name) <=16):
            raise Exception("Magazine's name must be between 2 and 16 characters, inclusive.")
        
        self._name = new_name

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str):
            raise Exception("Magazine's category should be a string.")
        if len(new_category) == 0:
            raise Exception("Magazine category must be longer than 0 characters")
        
        self._category = new_category

    @property
    def title(self):
         return self._title   
    
    @title.setter
    def set_title(self, new_title):
        if hasattr(self, "_title"):
            raise Exception("Cannot change title after it is set.")

        self._title = new_title

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT articles.title, articles.content
            FROM articles
            WHERE articles.magazine_id = ?
        """

        cursor.execute(sql, (self._id,))
        articles_list = cursor.fetchall()
        conn.close()

        if articles_list:
            return articles_list
        else:
            return None
        
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT authors.name
            FROM authors
            JOIN articles
            ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.name
        """

        cursor.execute(sql, (self._id,))
        contributors_list = cursor.fetchall()
        conn.close()

        if contributors_list:
            return contributors_list
        else:
            return None
    
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT articles.title
            FROM articles
            WHERE articles.magazine_id = ?
        """

        cursor.execute(sql, (self._id,))
        titles_list = [row[0] for row in cursor.fetchall()]
        conn.close()

        if titles_list:
            return titles_list
        else:
            return None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles
            ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        """

        cursor.execute(sql, (self._id))
        authors_list = cursor.fetchall()
        conn.close()
        
        if authors_list:
            contributing_authors = [Author(author[1], author[0]) for author in authors_list]
            return contributing_authors
        else:
            return None