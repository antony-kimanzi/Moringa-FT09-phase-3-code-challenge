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
    author = Author(name = author_name)

    # Create a magazine
    magazine = Magazine(name = magazine_name, category = magazine_category)

    # Create an article
    article = Article(author = author, magazine = magazine, title = article_title)

    article.add_content(article_content)

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models
     # Display created data
    print("\n--- Created Author ---")
    print(author)

    print("\n--- Created Magazine ---")
    print(magazine)

    print("\n--- Created Article ---")
    print(article)

    # Test Author methods
    print("\n--- Articles by Author ---")
    for art in author.articles():
        print(art)

    print("\n--- Magazines by Author ---")
    for mag in author.magazines():
        print(mag)

    # Test Magazine methods
    print("\n--- Articles in Magazine ---")
    for art in magazine.articles():
        print(art)

    print("\n--- Contributors to Magazine ---")
    for contrib in magazine.contributors():
        print(contrib)

    print("\n--- Article Titles in Magazine ---")
    for title in magazine.article_titles():
        print(title)

    print("\n--- Contributing Authors to Magazine ---")
    for contrib_author in magazine.contributing_authors():
        print(contrib_author)

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(id = magazine["id"], name = magazine["name"], category = magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(id = author["id"], name = author["name"]))

    print("\nArticles:")
    for article in articles:
        print(Article(id = article["id"], title=article["title"], author = article["author_id"], magazine = article["magazine_id"]))



if __name__ == "__main__":
    main()
