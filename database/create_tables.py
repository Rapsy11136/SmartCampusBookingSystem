from db_manager import Database


def create_tables():

    db = Database()

    # =========================
    # USERS
    # =========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL,

        campus_id INTEGER,

        FOREIGN KEY(campus_id)
        REFERENCES campuses(id)

    )
    """)

    # =========================
    # CAMPUSES
    # =========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS campuses(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE NOT NULL,

        max_duration INTEGER,

        opening_time TEXT,

        closing_time TEXT

    )
    """)

    # =========================
    # RESOURCES
    # =========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS resources(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        campus_id INTEGER NOT NULL,

        name TEXT NOT NULL,

        type TEXT NOT NULL,

        status TEXT DEFAULT 'Available',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(campus_id)
        REFERENCES campuses(id)

    )
    """)

    # =========================
    # BOOKINGS
    # =========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS bookings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        lecturer_id INTEGER NOT NULL,

        resource_id INTEGER NOT NULL,

        booking_date DATE NOT NULL,

        start_time TEXT NOT NULL,

        end_time TEXT NOT NULL,

        purpose TEXT NOT NULL,

        status TEXT DEFAULT 'Pending',

        approved_by INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(lecturer_id)
        REFERENCES users(id),

        FOREIGN KEY(resource_id)
        REFERENCES resources(id),

        FOREIGN KEY(approved_by)
        REFERENCES users(id)

    )
    """)

    db.close()

    print("Tables created successfully.")