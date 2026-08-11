from db_manager import Database


class BookingService:

    def __init__(self):
        self.db = Database()

    # -------------------------------------------------
    # CAMPUSES
    # -------------------------------------------------

    def get_campuses(self):

        return self.db.fetchall("""
            SELECT
                id,
                name,
                opening_time,
                closing_time
            FROM campuses
            ORDER BY name
        """)

    def get_campus(self, campus_id):

        return self.db.fetchone("""
            SELECT
                id,
                name,
                max_duration,
                opening_time,
                closing_time
            FROM campuses
            WHERE id=?
        """, (campus_id,))

    # -------------------------------------------------
    # RESOURCES
    # -------------------------------------------------

    def get_resources_by_campus(self, campus_id):

        return self.db.fetchall("""
            SELECT
                id,
                name,
                type,
                status
            FROM resources
            WHERE campus_id=?
            AND status='Available'
            ORDER BY name
        """, (campus_id,))

    def get_resources(self, campus_id):

        return self.db.fetchall("""

            SELECT
                id,
                name

            FROM resources

            WHERE
                campus_id=?
                AND status='Available'

            ORDER BY name

        """, (campus_id,))

    # -------------------------------------------------
    # CREATE BOOKING
    # -------------------------------------------------

    def create_booking(
            self,
            lecturer_id,
            campus_id,
            resource_id,
            booking_date,
            start_time,
            end_time,
            purpose
    ):

        # -----------------------------
        # Required fields
        # -----------------------------

        if not campus_id:
            return False, "Please select a campus."

        if not resource_id:
            return False, "Please select a resource."

        if not booking_date:
            return False, "Please select a booking date."

        if not start_time or not end_time:
            return False, "Please select the start and end time."

        if not purpose.strip():
            return False, "Please enter the booking purpose."

        # -----------------------------
        # Weekend validation
        # -----------------------------

        try:
            from datetime import datetime

            date_object = datetime.strptime(
                booking_date,
                "%Y-%m-%d"
            )

        except ValueError:
            return False, "Invalid booking date."

        if date_object.weekday() >= 5:
            return False, "Bookings are not allowed on weekends."

        # -----------------------------
        # Check lecturer campus
        # -----------------------------

        lecturer = self.db.fetchone("""
            SELECT campus_id
            FROM users
            WHERE id=?
        """, (lecturer_id,))

        if not lecturer:
            return False, "Lecturer account could not be found."

        lecturer_campus_id = lecturer[0]

        if lecturer_campus_id is None:
            return False, (
                "Your account has no campus assigned. "
                "Please contact the administrator."
            )

        if lecturer_campus_id != campus_id:
            return False, (
                "You can only book resources "
                "from your assigned campus."
            )

        # -----------------------------
        # Check resource belongs to campus
        # -----------------------------

        resource = self.db.fetchone("""
            SELECT
                id,
                name,
                campus_id,
                status
            FROM resources
            WHERE id=?
        """, (resource_id,))

        if not resource:
            return False, "Selected resource does not exist."

        if resource[2] != campus_id:
            return False, (
                "This resource does not belong "
                "to your selected campus."
            )

        if resource[3] != "Available":
            return False, "This resource is not available."

        # -----------------------------
        # Time validation
        # -----------------------------

        if start_time >= end_time:
            return False, (
                "End time must be later than start time."
            )

        # -----------------------------
        # Campus operating hours
        # -----------------------------

        campus = self.get_campus(campus_id)

        if not campus:
            return False, "Campus could not be found."

        opening_time = campus[3]
        closing_time = campus[4]

        if start_time < opening_time:
            return False, (
                f"Booking cannot start before {opening_time}."
            )

        if end_time > closing_time:
            return False, (
                f"Booking must end by {closing_time}."
            )

        # -----------------------------
        # Maximum 2 bookings per day
        # -----------------------------

        daily_count = self.db.fetchone("""
            SELECT COUNT(*)
            FROM bookings
            WHERE lecturer_id=?
            AND booking_date=?
            AND status!='Cancelled'
        """, (
            lecturer_id,
            booking_date
        ))

        if daily_count[0] >= 2:
            return False, (
                "You can only make a maximum "
                "of 2 bookings per day."
            )

        # -----------------------------
        # Check overlapping booking
        # -----------------------------

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
        """, (
            resource_id,
            booking_date,
            end_time,
            start_time
        ))

        if conflict:
            return False, (
                "This resource is already booked "
                "during that time."
            )

        # -----------------------------
        # Create booking
        # -----------------------------

        self.db.execute("""
            INSERT INTO bookings(
                lecturer_id,
                resource_id,
                booking_date,
                start_time,
                end_time,
                purpose,
                status
            )
            VALUES(?,?,?,?,?,?,?)
        """, (
            lecturer_id,
            resource_id,
            booking_date,
            start_time,
            end_time,
            purpose.strip(),
            "Pending"
        ))

        return True, "Booking created successfully and is awaiting approval."

    # -------------------------------------------------
    # LECTURER BOOKINGS
    # -------------------------------------------------

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

    # -------------------------------------------------
    # CANCEL BOOKING
    # -------------------------------------------------

    def cancel_booking(self, booking_id):

        self.db.execute("""
            UPDATE bookings
            SET status='Cancelled'
            WHERE id=?
            AND status='Pending'
        """, (booking_id,))

    # -------------------------------------------------
    # ADMIN APPROVALS
    # -------------------------------------------------

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

            ORDER BY
                bookings.booking_date ASC,
                bookings.start_time ASC
        """)

    def approve_booking(self, booking_id, admin_id):

        self.db.execute("""
            UPDATE bookings

            SET
                status='Approved',
                approved_by=?

            WHERE id=?
            AND status='Pending'
        """, (
            admin_id,
            booking_id
        ))

        return True, "Booking approved successfully."

    def reject_booking(self, booking_id, admin_id):

        self.db.execute("""
            UPDATE bookings

            SET
                status='Rejected',
                approved_by=?

            WHERE id=?
            AND status='Pending'
        """, (
            admin_id,
            booking_id
        ))

        return True, "Booking rejected successfully."