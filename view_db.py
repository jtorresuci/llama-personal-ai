import sqlite3

def view_database():
    conn = sqlite3.connect('email_summaries.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)
    
    # View contents of the emails table
    cursor.execute("SELECT * FROM emails LIMIT 5")
    rows = cursor.fetchall()
    
    print("\nSample data from emails table:")
    for row in rows:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    view_database()