from database.connection import get_db_connection



class Author:
    def __init__(self, name, id = None):     
        if not isinstance(name, str):
            raise Exception("Author's name should be a string.")
        if len(name) == 0:
            raise Exception("Author's name must be longer than zero characters.")   
        self._name = name
        self._id = id

        if id is None:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO authors (name) VALUES (?)"
            cursor.execute(sql, (name,))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def set_name(self, new_name):
        if hasattr(self, "_name"):
            raise Exception("Author's name already exists.")
        
        self._name = new_name

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT articles.id, articles.title, articles.content
            FROM articles
            JOIN authors
            ON articles.author_id = authors.id
            WHERE articles.author_id = ?
        """

        cursor.execute(sql, (self._id,))
        articles_list = cursor.fetchall()
        conn.close()

        if articles_list:
            return articles_list
        else:
            return None
        
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT magazines.id, magazines.name, magazines.author
            FROM magazines
            JOIN articles
            ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
            GROUP BY magazines.id, magazines.name, magazines.author
        """

        cursor.execute(sql, (self._id))
        magazines_list = cursor.fetchall()
        conn.close()

        return magazines_list

