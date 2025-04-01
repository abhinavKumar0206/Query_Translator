import sqlite3
from datetime import datetime, timedelta
import random
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect('data/t_shirt_sales.db')
cursor = conn.cursor()

# Drop tables if they exist (clean slate)
cursor.execute("DROP TABLE IF EXISTS Returns")
cursor.execute("DROP TABLE IF EXISTS Sales")
cursor.execute("DROP TABLE IF EXISTS Inventory")
cursor.execute("DROP TABLE IF EXISTS Products")

# Create Products table
cursor.execute("""
CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    color TEXT,
    size TEXT,
    price DECIMAL(10,2),
    launch_date DATE
)
""")

# Create Sales table
cursor.execute("""
CREATE TABLE Sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    date DATE,
    quantity INTEGER,
    region TEXT,
    discount DECIMAL(5,2) DEFAULT 0.0,
    FOREIGN KEY (product_id) REFERENCES Products(id)
)
""")

# Create Returns table
cursor.execute("""
CREATE TABLE Returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER,
    reason TEXT,
    date DATE,
    FOREIGN KEY (sale_id) REFERENCES Sales(id)
)
""")

# Create Inventory table
cursor.execute("""
CREATE TABLE Inventory (
    product_id INTEGER PRIMARY KEY,
    stock_level INTEGER,
    last_restock DATE,
    FOREIGN KEY (product_id) REFERENCES Products(id)
)
""")

# Sample product data
products = [
    ('Vintage Logo', 'Men', 'Black', 'M', 24.99, '2023-01-15'),
    ('Modern Fit', 'Women', 'White', 'S', 19.99, '2023-02-10'),
    ('Classic Crew', 'Unisex', 'Navy', 'L', 22.50, '2023-01-20'),
    ('Graphic Print', 'Men', 'Red', 'XL', 27.99, '2023-03-05'),
    ('Athletic Dry-Fit', 'Women', 'Blue', 'M', 29.99, '2023-02-28'),
    ('Pocket Tee', 'Unisex', 'Gray', 'S', 21.50, '2023-03-15'),
    ('Oversized Fit', 'Women', 'Pink', 'L', 26.99, '2023-04-01'),
    ('Muscle Fit', 'Men', 'Black', 'L', 25.50, '2023-03-20'),
    ('Longline', 'Unisex', 'Olive', 'M', 28.99, '2023-04-10'),
    ('Cropped', 'Women', 'Yellow', 'XS', 23.99, '2023-05-05')
]

cursor.executemany("""
INSERT INTO Products (name, category, color, size, price, launch_date)
VALUES (?, ?, ?, ?, ?, ?)
""", products)

# Generate sales data
regions = ['North', 'South', 'East', 'West', 'International']
today = datetime.now()
start_date = today - timedelta(days=180)

for _ in range(500):
    product_id = random.randint(1, len(products))
    sale_date = start_date + timedelta(days=random.randint(0, 180))
    quantity = random.randint(1, 3)
    region = random.choice(regions)
    discount = round(random.uniform(0, 0.3) if random.random() < 0.2 else 0, 2)
    
    cursor.execute("""
    INSERT INTO Sales (product_id, date, quantity, region, discount)
    VALUES (?, ?, ?, ?, ?)
    """, (product_id, sale_date.strftime('%Y-%m-%d'), quantity, region, discount))

# Generate returns data
cursor.execute("SELECT id FROM Sales")
sales_ids = [row[0] for row in cursor.fetchall()]
return_reasons = ['Size issue', 'Color mismatch', 'Changed mind', 'Quality problem', 'Delivery delay']

for sale_id in random.sample(sales_ids, int(len(sales_ids) * 0.08)):
    cursor.execute("SELECT date FROM Sales WHERE id = ?", (sale_id,))
    sale_date = cursor.fetchone()[0]
    return_date = datetime.strptime(sale_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 14))
    reason = random.choice(return_reasons)
    
    cursor.execute("""
    INSERT INTO Returns (sale_id, reason, date)
    VALUES (?, ?, ?)
    """, (sale_id, reason, return_date.strftime('%Y-%m-%d')))

# Generate inventory data
for product_id in range(1, len(products) + 1):
    stock_level = random.randint(10, 100)
    last_restock = today - timedelta(days=random.randint(1, 30))
    
    cursor.execute("""
    INSERT INTO Inventory (product_id, stock_level, last_restock)
    VALUES (?, ?, ?)
    """, (product_id, stock_level, last_restock.strftime('%Y-%m-%d')))

# Commit and close
conn.commit()
conn.close()

print("Database successfully created at data/t_shirt_sales.db")