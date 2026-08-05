from db_manager import Database


class CampusService:

    def __init__(self):
        self.db = Database()

    def get_campuses(self):
        return self.db.fetchall("""
            SELECT
                id,
                name,
                max_duration,
                opening_time,
                closing_time
            FROM campuses
            ORDER BY name
        """)

    def add_campus(
        self,
        name,
        max_duration,
        opening_time,
        closing_time
    ):

        self.db.execute("""
            INSERT INTO campuses
            (
                name,
                max_duration,
                opening_time,
                closing_time
            )
            VALUES(?,?,?,?)
        """,
        (
            name,
            max_duration,
            opening_time,
            closing_time
        ))

    def update_campus(
        self,
        campus_id,
        name,
        max_duration,
        opening_time,
        closing_time
    ):

        self.db.execute("""
            UPDATE campuses

            SET

                name=?,
                max_duration=?,
                opening_time=?,
                closing_time=?

            WHERE id=?
        """,
        (
            name,
            max_duration,
            opening_time,
            closing_time,
            campus_id
        ))

    def delete_campus(self, campus_id):

        self.db.execute("""
            DELETE FROM campuses
            WHERE id=?
        """, (campus_id,))

    def search_campuses(self, keyword):

        keyword = f"%{keyword}%"

        return self.db.fetchall("""
            SELECT
                id,
                name,
                max_duration,
                opening_time,
                closing_time
            FROM campuses
            WHERE name LIKE ?
            ORDER BY name
        """, (keyword,))