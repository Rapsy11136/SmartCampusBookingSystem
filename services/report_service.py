from db_manager import Database


class ReportService:

    def __init__(self):
        self.db = Database()

    def get_statistics(self):

        total = self.db.fetchone(
            "SELECT COUNT(*) FROM bookings"
        )[0]

        pending = self.db.fetchone(
            "SELECT COUNT(*) FROM bookings WHERE status='Pending'"
        )[0]

        approved = self.db.fetchone(
            "SELECT COUNT(*) FROM bookings WHERE status='Approved'"
        )[0]

        rejected = self.db.fetchone(
            "SELECT COUNT(*) FROM bookings WHERE status='Rejected'"
        )[0]

        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected
        }

    def get_all_bookings(self):

        return self.db.fetchall("""

            SELECT

                bookings.id,

                users.fullname,

                campuses.name,

                resources.name,

                bookings.booking_date,

                bookings.status

            FROM bookings

            JOIN users
                ON bookings.lecturer_id = users.id

            JOIN resources
                ON bookings.resource_id = resources.id

            JOIN campuses
                ON resources.campus_id = campuses.id

            ORDER BY bookings.booking_date DESC

        """)