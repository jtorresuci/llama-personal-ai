from src.database import EmailDatabase

db = EmailDatabase()
db.export_to_csv()
db.close()