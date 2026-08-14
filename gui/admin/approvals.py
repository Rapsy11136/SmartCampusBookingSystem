import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

from services.booking_service import BookingService


class ApprovalFrame(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(master)

        self.user = user
        self.service = BookingService()

        # ==============================
        # TITLE
        # ==============================

        ctk.CTkLabel(
            self,
            text="Booking Approvals",
            font=("Arial", 28, "bold")
        ).pack(
            pady=(20, 10)
        )

        # ==============================
        # TOOLBAR
        # ==============================

        toolbar = ctk.CTkFrame(self)

        toolbar.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.load_bookings
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="Approve",
            fg_color="green",
            hover_color="#006400",
            command=self.approve_booking
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="Reject",
            fg_color="red",
            hover_color="#B22222",
            command=self.reject_booking
        ).pack(
            side="right",
            padx=5
        )

        # ==============================
        # TABLE
        # ==============================

        columns = (
            "ID",
            "Lecturer",
            "Campus",
            "Resource",
            "Date",
            "Start",
            "End",
            "Status"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=16
        )

        widths = {
            "ID": 60,
            "Lecturer": 150,
            "Campus": 130,
            "Resource": 140,
            "Date": 110,
            "Start": 80,
            "End": 80,
            "Status": 100
        }

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_bookings()

    # ==============================
    # LOAD BOOKINGS
    # ==============================

    def load_bookings(self):

        for row in self.table.get_children():
            self.table.delete(row)

        bookings = self.service.get_pending_bookings()

        # Campus administrators should only see
        # bookings for their own campus.

        if str(self.user[4]).lower() == "campus administrator":

            campus_id = self.user[5]

            filtered = []

            for booking in bookings:

                # booking structure:
                # ID, Lecturer, Campus, Resource,
                # Date, Start, End, Status

                campus_name = booking[2]

                campus = self.service.db.fetchone("""
                    SELECT name
                    FROM campuses
                    WHERE id=?
                """, (campus_id,))

                if campus and campus_name == campus[0]:

                    filtered.append(booking)

            bookings = filtered

        for booking in bookings:

            self.table.insert(
                "",
                "end",
                values=booking
            )

    # ==============================
    # GET SELECTED BOOKING
    # ==============================

    def get_selected_booking(self):

        selected = self.table.selection()

        if not selected:

            CTkMessagebox(
                title="No Selection",
                message="Please select a booking first.",
                icon="warning"
            )

            return None

        values = self.table.item(
            selected[0]
        )["values"]

        return values

    # ==============================
    # APPROVE
    # ==============================

    def approve_booking(self):

        booking = self.get_selected_booking()

        if booking is None:
            return

        booking_id = booking[0]

        success, message = self.service.approve_booking(
            booking_id,
            self.user[0]
        )

        CTkMessagebox(
            title="Approval",
            message=message,
            icon="check" if success else "warning"
        )

        self.load_bookings()

    # ==============================
    # REJECT
    # ==============================

    def reject_booking(self):

        booking = self.get_selected_booking()

        if booking is None:
            return

        booking_id = booking[0]

        success, message = self.service.reject_booking(
            booking_id
        )

        CTkMessagebox(
            title="Rejection",
            message=message,
            icon="check" if success else "warning"
        )

        self.load_bookings()