import sqlite3


class DBConnection:
    def __init__(self, db_name='products.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return self
        except sqlite3.Error as e:
            # Handle the error, print or log the error message
            print("Error while connecting to the database:", e)
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    image_url TEXT
                )
            ''')
        except sqlite3.Error as e:
            # Handle the error, print or log the error message
            print("Error while creating table:", e)
            raise e

    def insert_product(self, title, image_url):
        try:
            self.cursor.execute('INSERT INTO products (title, image_url) VALUES (?, ?)', (title, image_url))
        except sqlite3.Error as e:
            # Handle the error, print or log the error message
            print("Error while inserting product:", e)
            raise e

    def get_all_products(self):
        try:
            self.cursor.execute('SELECT title, image_url FROM products')
            products = [{'title': title, 'image_url': image_url} for title, image_url in self.cursor.fetchall()]
            return products
        except sqlite3.Error as e:
            # Handle the error, print or log the error message
            print("Error while retrieving products:", e)
            raise e
