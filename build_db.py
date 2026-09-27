import sqlite3
import pandas as pd
import os

def build_database():
    db_path = 'pharmeasy.db'
    
    # Resolve paths
    orders_path = '/content/orders_clean.csv' if os.path.exists('/content/orders_clean.csv') else 'orders_clean.csv'
    regions_path = '/content/regions_master.csv' if os.path.exists('/content/regions_master.csv') else 'regions_master.csv'
    
    # Load datasets
    df_orders = pd.read_csv(orders_path)
    df_regions = pd.read_csv(regions_path)
    
    # Establish SQLite connection
    conn = sqlite3.connect(db_path)
    
    # Write tables to the database
    df_orders.to_sql('orders_clean', conn, if_exists='replace', index=False)
    df_regions.to_sql('regions_master', conn, if_exists='replace', index=False)
    
    # Verify database setup
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Created tables in {db_path}: {[t[0] for t in tables]}")
    
    cursor.execute("SELECT count(*) FROM orders_clean;")
    orders_count = cursor.fetchone()[0]
    print(f"Rows in orders_clean: {orders_count}")
    
    cursor.execute("SELECT count(*) FROM regions_master;")
    regions_count = cursor.fetchone()[0]
    print(f"Rows in regions_master: {regions_count}")
    
    conn.close()

build_database()