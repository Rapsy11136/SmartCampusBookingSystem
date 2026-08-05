import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

from services.booking_service import BookingService


class MyBookingsFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user
        self.service = BookingService()

        title = ctk.CTkLabel(
            self,
            text="My Bookings",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=20, pady=10)

        self.search = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search..."
        )
        self.search.pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.load_bookings
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Cancel Booking",
            fg_color="red",
            command=self.cancel_booking
        ).pack(side="right", padx=5)

        columns = (
            "ID",
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
            height=15
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=120)

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_bookings()

    def load_bookings(self):

        for item in self.table.get_children():
            self.table.delete(item)

        bookings = self.service.get_bookings_by_lecturer(
            self.user[0]
        )

        for booking in bookings:
            self.table.insert("", "end", values=booking)

    def cancel_booking(self):

        selected = self.table.selection()

        if not selected:
            CTkMessagebox(
                title="No Selection",
                message="Please select a booking."
            )

            return

        booking = self.table.item(selected[0])["values"]

        booking_id = booking[0]

        status = booking[6]

        if status != "Pending":
            CTkMessagebox(
                title="Not Allowed",
                message="Only pending bookings can be cancelled."
            )

            return

        self.service.cancel_booking(booking_id)

        CTkMessagebox(
            title="Success",
            message="Booking cancelled successfully.",
            icon="check"
        )

        self.load_bookings()