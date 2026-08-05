from db_manager import Database

db = Database()

print("=== BOOKINGS TABLE ===")

columns = db.fetchall("PRAGMA table_info(bookings)")

for column in columns:
    print(column)

db.close()