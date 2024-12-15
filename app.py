from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():


    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author
    author = Author(author_name)

    # Create a magazine
    magazine = Magazine(magazine_name, magazine_category)

    # Create an article
    article = Article(author, magazine, article_title)

    article.add_content(article_content)

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    # print("\nMagazines:")
    # for magazine in magazines:
    #     print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    # print("\nAuthors:")
    # for author in authors:
    #     print(Author(author["id"], author["name"]))

    # print("\nArticles:")
    # for article in articles:
    #     print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

if __name__ == "__main__":
    main()
