import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize
fake = Faker()
conn = sqlite3.connect('data/new_database.db')
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    customer_name TEXT,
    order_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

# Insert sample data
categories = ['Electronics', 'Books', 'Home', 'Clothing']
for _ in range(50):
    cursor.execute(
        "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
        (fake.word().capitalize() + " " + fake.word(), 
         random.choice(categories),
         round(random.uniform(10, 500), 2))
    )

for _ in range(200):
    cursor.execute(
        "INSERT INTO orders (product_id, quantity, customer_name, order_date) VALUES (?, ?, ?, ?)",
        (random.randint(1, 50),
         random.randint(1, 5),
         fake.name(),
         (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'))
    )

conn.commit()
conn.close()
print("New database created at data/new_database.db with sample data")