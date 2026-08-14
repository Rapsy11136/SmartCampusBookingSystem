from db_manager import Database
from datetime import datetime


class BookingService:

    def __init__(self):

        self.db = Database()

    # =========================================================
    # GET AVAILABLE RESOURCES
    # =========================================================

    def get_resources(self):

        return self.db.fetchall("""
            SELECT
                id,
                name
            FROM resources
            WHERE status='Available'
            ORDER BY name
        """)

    # =========================================================
    # CREATE BOOKING
    # =========================================================

    def create_booking(
            self,
            lecturer_id,
            resource_id,
            booking_date,
            start_time,
            end_time,
            purpose
    ):

        # =====================================================
        # VALIDATE DATE
        # =====================================================

        try:

            selected_date = datetime.strptime(
                booking_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return False, "Invalid booking date."

        today = datetime.now().date()

        # =====================================================
        # PAST DATE
        # =====================================================

        if selected_date < today:

            return False, "You cannot book a past date."

        # =====================================================
        # WEEKEND
        # =====================================================

        if selected_date.weekday() >= 5:

            return False, (
                "Bookings are not allowed on weekends."
            )

        # =====================================================
        # VALIDATE TIMES
        # =====================================================

        try:

            start = datetime.strptime(
                start_time,
                "%H:%M"
            )

            end = datetime.strptime(
                end_time,
                "%H:%M"
            )

        except ValueError:

            return False, "Invalid booking time."

        # =====================================================
        # START BEFORE END
        # =====================================================

        if start >= end:

            return False, (
                "Start time must be earlier than end time."
            )

        # =====================================================
        # 14:00 CUTOFF
        # =====================================================

        cutoff = datetime.strptime(
            "14:00",
            "%H:%M"
        )

        if end > cutoff:

            return False, (
                "Bookings cannot continue after 14:00."
            )

        # =====================================================
        # PURPOSE
        # =====================================================

        if not purpose or not purpose.strip():

            return False, (
                "Booking purpose is required."
            )

        # =====================================================
        # MAXIMUM 2 BOOKINGS PER DAY
        # =====================================================

        daily_count = self.db.fetchone("""
            SELECT COUNT(*)
            FROM bookings
            WHERE
                lecturer_id=?
                AND booking_date=?
                AND status!='Cancelled'
        """, (
            lecturer_id,
            booking_date
        ))

        if daily_count and daily_count[0] >= 2:

            return False, (
                "You can only make a maximum of "
                "2 bookings per day."
            )

        # =====================================================
        # RESOURCE CONFLICT
        # =====================================================

        conflict = self.db.fetchone("""
            SELECT id
            FROM bookings
            WHERE
                resource_id=?
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

        # =====================================================
        # INSERT BOOKING
        # =====================================================

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
        """, (
            lecturer_id,
            resource_id,
            booking_date,
            start_time,
            end_time,
            purpose.strip()
        ))

        return True, "Booking created successfully."

    # =========================================================
    # GET LECTURER BOOKINGS
    # =========================================================

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
        """, (
            lecturer_id,
        ))

    # =========================================================
    # CANCEL BOOKING
    # =========================================================

    def cancel_booking(self, booking_id):

        self.db.execute("""
            UPDATE bookings
            SET status='Cancelled'
            WHERE id=?
            AND status='Pending'
        """, (
            booking_id,
        ))

    # =========================================================
    # GET PENDING BOOKINGS
    # =========================================================

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

    def approve_booking(self, booking_id, approved_by):

        self.db.execute("""
            UPDATE bookings

            SET
                status='Approved',
                approved_by=?

            WHERE
                id=?
                AND status='Pending'
        """, (
            approved_by,
            booking_id
        ))

        return True, "Booking approved successfully."

    def reject_booking(self, booking_id):

        self.db.execute("""
            UPDATE bookings

            SET status='Rejected'

            WHERE
                id=?
                AND status='Pending'
        """, (
            booking_id,
        ))

        return True, "Booking rejected successfully."

    # =========================================================
    # APPROVE BOOKING
    # =========================================================

    def approve_booking(
            self,
            booking_id,
            approved_by
    ):

        self.db.execute("""
            UPDATE bookings

            SET
                status='Approved',
                approved_by=?

            WHERE
                id=?
                AND status='Pending'
        """, (
            approved_by,
            booking_id
        ))

        return True, "Booking approved successfully."

    # =========================================================
    # REJECT BOOKING
    # =========================================================

    def reject_booking(self, booking_id):

        self.db.execute("""
            UPDATE bookings

            SET status='Rejected'

            WHERE
                id=?
                AND status='Pending'
        """, (
            booking_id,
        ))

        return True, "Booking rejected successfully."