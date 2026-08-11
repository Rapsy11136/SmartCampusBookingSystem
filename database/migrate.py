from db_manager import Database


def column_exists(db, table_name, column_name):

    columns = db.fetchall(
        f"PRAGMA table_info({table_name})"
    )

    return any(column[1] == column_name for column in columns)


def migrate_database():

    db = Database()

    # Add campus_id to users
    if not column_exists(db, "users", "campus_id"):

        db.execute("""
        ALTER TABLE users
        ADD COLUMN campus_id INTEGER
        """)

        print("Added users.campus_id")

    # Add booking cutoff to campuses
    if not column_exists(
            db,
            "campuses",
            "booking_cutoff_time"
    ):

        db.execute("""
        ALTER TABLE campuses
        ADD COLUMN booking_cutoff_time TEXT
        """)

        db.execute("""
        UPDATE campuses
        SET booking_cutoff_time='14:00'
        WHERE booking_cutoff_time IS NULL
        """)

        print("Added campuses.booking_cutoff_time")

    # Give existing campuses different policies
    db.execute("""
    UPDATE campuses
    SET
        max_duration=2,
        opening_time='08:00',
        closing_time='17:00',
        booking_cutoff_time='14:00'
    WHERE name='Pretoria'
    """)

    db.execute("""
    UPDATE campuses
    SET
        max_duration=3,
        opening_time='07:30',
        closing_time='18:00',
        booking_cutoff_time='15:00'
    WHERE name='Johannesburg'
    """)

    db.execute("""
    UPDATE campuses
    SET
        max_duration=4,
        opening_time='08:00',
        closing_time='16:00',
        booking_cutoff_time='13:30'
    WHERE name='Polokwane'
    """)

    db.close()

    print("Database migration completed successfully.")


if __name__ == "__main__":
    migrate_database()