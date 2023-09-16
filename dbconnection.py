import sqlite3


class DBConnection:
    def __init__(self, db_name='products.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                image_url TEXT
            )
        ''')
        self.conn.commit()

    def insert_product(self, title, image_url):
        # self.cursor.execute('INSERT INTO products (title, image_url) VALUES (?, ?)', (title, image_url))
        # self.conn.commit()
        try:
            self.cursor.execute('INSERT INTO products (title, image_url) VALUES (?, ?)', (title, image_url))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error while inserting product:", e)  # Debugging statement
            raise e

    def get_all_products(self):
        try:
            self.cursor.execute('SELECT title, image_url FROM products')
            products = [{'title': title, 'image_url': image_url} for title, image_url in self.cursor.fetchall()]
            return products
        except sqlite3.Error as e:
            print("Error while retrieving products:", e)  # Debugging statement
            raise e
