from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    try:
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

        # Create an author
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
        author_id = cursor.lastrowid
        
        # Create a magazine
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
        magazine_id = cursor.lastrowid
        
        # Create an article
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (article_title, article_content, author_id, magazine_id))
        
        conn.commit()

        # Query the database for inserted records
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
            print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

        print("\nAuthors:")
        for author in authors:
            print(Author(author["id"], author["name"]))

        print("\nArticles:")
        for article in articles:
            print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

        # Test Magazine class
        print("\nTesting Magazine Class:")
        magazine_instance = Magazine()
        magazine_instance.name = "Science Today"
        magazine_instance.category = "Science"
        magazine_instance.save()
        print(f"Magazine ID: {magazine_instance.id}")
        print(f"Magazine Name: {magazine_instance.name}")
        print(f"Magazine Category: {magazine_instance.category}")
        print("Article Titles:", magazine_instance.article_titles())
        print("Contributing Authors:", magazine_instance.contributing_authors())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
