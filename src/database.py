import sqlite3
from datetime import datetime

class EmailDatabase:
    def __init__(self, db_file='email_summaries.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            date_received TEXT,
            subject TEXT,
            summary TEXT,
            date_analyzed TIMESTAMP,
            PRIMARY KEY (date_received, subject)
        )
        ''')
        self.conn.commit()

    def email_exists(self, date_received, subject):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM emails WHERE date_received = ? AND subject = ?', (date_received, subject))
        return cursor.fetchone() is not None

    def add_email(self, date_received, subject, summary):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO emails (date_received, subject, summary, date_analyzed)
        VALUES (?, ?, ?, ?)
        ''', (date_received, subject, summary, datetime.now()))
        self.conn.commit()

    def get_recent_summaries(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT date_received, subject, summary FROM emails
        ORDER BY date_analyzed DESC
        LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    def export_to_csv(self, filename='email_summaries.csv'):
        import csv
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM emails ORDER BY date_analyzed DESC')
        entries = cursor.fetchall()

        if not entries:
            print("No entries in the database to export.")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date Received', 'Subject', 'Summary', 'Date Analyzed'])
            csv_writer.writerows(entries)

        print(f"Data exported to {filename}")

    def close(self):
        self.conn.close()