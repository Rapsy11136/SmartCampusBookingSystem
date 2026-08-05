from db_manager import Database


def seed_database():
    db = Database()

    campuses = [
        ("Pretoria", 2, "08:00", "17:00"),
        ("Johannesburg", 3, "07:30", "18:00"),
        ("Polokwane", 4, "08:00", "16:00")
    ]

    for campus in campuses:
        db.execute("""
        INSERT OR IGNORE INTO campuses
        (name, max_duration, opening_time, closing_time)
        VALUES (?, ?, ?, ?)
        """, campus)

    db.close()

    print("Database seeded successfully.")