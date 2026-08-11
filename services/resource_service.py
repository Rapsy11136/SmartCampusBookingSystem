from db_manager import Database

class ResourceService:

    def __init__(self):
        self.db = Database()


    def get_all_resources(self):
        return self.db.fetchall("""
            SELECT
                resources.id,
                campuses.name,
                resources.name,
                resources.type,
                resources.status
            FROM resources
            JOIN campuses
            ON campuses.id = resources.campus_id
            ORDER BY campuses.name, resources.name
        """)

    def get_campuses(self):
        return self.db.fetchall("""
            SELECT id, name
            FROM campuses
            ORDER BY name
        """)

    def add_resource(self, campus_id, name, resource_type):

        self.db.execute("""
            INSERT INTO resources
            (campus_id, name, type, status)
            VALUES (?, ?, ?, ?)
        """, (
            campus_id,
            name,
            resource_type,
            "Available"
        ))

    def delete_resource(self, resource_id):

        self.db.execute("""
            DELETE FROM resources
            WHERE id=?
        """, (resource_id,))

    def search_resources(self, keyword):

        keyword = f"%{keyword}%"

        return self.db.fetchall("""
            SELECT
                resources.id,
                campuses.name,
                resources.name,
                resources.type,
                resources.status
            FROM resources
            JOIN campuses
            ON campuses.id = resources.campus_id
            WHERE
                resources.name LIKE ?
                OR resources.type LIKE ?
                OR campuses.name LIKE ?
        """, (keyword, keyword, keyword))

    def total_resources(self):
        result = self.db.fetchone("""
            SELECT COUNT(*)
            FROM resources
        """)

        return result[0]

    def available_resources(self):
        result = self.db.fetchone("""
            SELECT COUNT(*)
            FROM resources
            WHERE status='Available'
        """)

        return result[0]

    def booked_resources(self):
        result = self.db.fetchone("""
            SELECT COUNT(*)
            FROM resources
            WHERE status='Booked'
        """)

        return result[0]

    def update_resource(
            self,
            resource_id,
            campus_id,
            name,
            resource_type,
            status
    ):
        self.db.execute(
            """
            UPDATE resources

            SET

                campus_id=?,
                name=?,
                type=?,
                status=?

            WHERE id=?
            """,
            (
                campus_id,
                name,
                resource_type,
                status,
                resource_id
            )
        )

    def get_resource(self, resource_id):
        return self.db.fetchone(
            """
            SELECT
                id,
                campus_id,
                name,
                type,
                status
            FROM resources
            WHERE id=?
            """,
            (resource_id,)
        )

    def get_campuses(self):
        return self.db.fetchall("""
            SELECT id, name
            FROM campuses
            ORDER BY name
        """)

    def get_resources_by_campus(self, campus_id):
        return self.db.fetchall("""

            SELECT id, name

            FROM resources

            WHERE campus_id=?
            AND status='Available'

            ORDER BY name

        """, (campus_id,))

    def get_available_resources_by_campus(self, campus_id):
        return self.db.fetchall("""
            SELECT
                id,
                name
            FROM resources
            WHERE campus_id=?
            AND status='Available'
            ORDER BY name
        """, (campus_id,))