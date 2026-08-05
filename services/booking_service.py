from db_manager import Database


class BookingService:

    def __init__(self):
        self.db = Database()

    # -----------------------------
    # Lecturer
    # -----------------------------

    def get_resources(self):

        return self.db.fetchall("""
            SELECT id, name
            FROM resources
            WHERE status='Available'
            ORDER BY name
        """)

    def create_booking(
        self,
        lecturer_id,
        resource_id,
        booking_date,
        start_time,
        end_time,
        purpose
    ):

        conflict = self.db.fetchone("""
            SELECT id
            FROM bookings
            WHERE resource_id=?
              AND booking_date=?
              AND status!='Cancelled'
              AND (
                    start_time < ?
                    AND end_time > ?
              )
        """,
        (
            resource_id,
            booking_date,
            end_time,
            start_time
        ))

        if conflict:
            return False, "This resource is already booked during that time."

        self.db.execute("""
            INSERT INTO bookings(
                lecturer_id,
                resource_id,
                booking_date,
                start_time,
                end_time,
                purpose
            )
            VALUES(?,?,?,?,?,?)
        """,
        (
            lecturer_id,
            resource_id,
            booking_date,
            start_time,
            end_time,
            purpose
        ))

        return True, "Booking created successfully."

    def get_bookings_by_lecturer(self, lecturer_id):

        return self.db.fetchall("""
            SELECT

                bookings.id,

                campuses.name,

                resources.name,

                bookings.booking_date,

                bookings.start_time,

                bookings.end_time,

                bookings.status

            FROM bookings

            JOIN resources
                ON bookings.resource_id = resources.id

            JOIN campuses
                ON resources.campus_id = campuses.id

            WHERE bookings.lecturer_id=?

            ORDER BY
                bookings.booking_date DESC,
                bookings.start_time DESC
        """, (lecturer_id,))

    def cancel_booking(self, booking_id):

        self.db.execute("""
            UPDATE bookings
            SET status='Cancelled'
            WHERE id=?
            AND status='Pending'
        """, (booking_id,))

    # -----------------------------
    # Campus Administrator
    # -----------------------------

    def get_pending_bookings(self):

        return self.db.fetchall("""

            SELECT

                bookings.id,

                users.fullname,

                campuses.name,

                resources.name,

                bookings.booking_date,

                bookings.start_time,

                bookings.end_time,

                bookings.status

            FROM bookings

            JOIN users
                ON bookings.lecturer_id = users.id

            JOIN resources
                ON bookings.resource_id = resources.id

            JOIN campuses
                ON campuses.id = resources.campus_id

            WHERE bookings.status='Pending'

            ORDER BY
                bookings.booking_date,
                bookings.start_time

        """)

<<<<<<< HEAD
    def approve_booking(self, booking_id, admin_id):

        self.db.execute("""

            UPDATE bookings

            SET
                status='Approved',
                approved_by=?

            WHERE id=?

        """, (admin_id, booking_id))

        self.db.execute("""

            UPDATE resources

            SET status='Booked'

            WHERE id=(

                SELECT resource_id

                FROM bookings

                WHERE id=?

            )

        """, (booking_id,))

    def reject_booking(self, booking_id, admin_id):

        self.db.execute("""

            UPDATE bookings

            SET
                status='Rejected',
                approved_by=?

            WHERE id=?

=======
    def get_pending_bookings(self):
        return self.db.fetchall("""
            SELECT
                bookings.id,
                users.fullname,
                campuses.name,
                resources.name,
                bookings.booking_date,
                bookings.start_time,
                bookings.end_time,
                bookings.status
            FROM bookings
            JOIN users
                ON bookings.lecturer_id = users.id
            JOIN resources
                ON bookings.resource_id = resources.id
            JOIN campuses
                ON resources.campus_id = campuses.id
            WHERE bookings.status='Pending'
            ORDER BY bookings.booking_date,
                     bookings.start_time
        """)

    def approve_booking(self, booking_id, admin_id):
        self.db.execute("""
            UPDATE bookings
            SET
                status='Approved',
                approved_by=?
            WHERE id=?
        """, (admin_id, booking_id))

        self.db.execute("""
            UPDATE resources
            SET status='Booked'
            WHERE id=(
                SELECT resource_id
                FROM bookings
                WHERE id=?
            )
        """, (booking_id,))

    def reject_booking(self, booking_id, admin_id):
        self.db.execute("""
            UPDATE bookings
            SET
                status='Rejected',
                approved_by=?
            WHERE id=?
>>>>>>> aa24f26 (fucntioning App)
        """, (admin_id, booking_id))