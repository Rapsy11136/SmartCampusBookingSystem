import customtkinter as ctk

from tkinter import ttk

from CTkMessagebox import CTkMessagebox

from services.booking_service import BookingService


class ApprovalFrame(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(master)

        self.user = user

        self.service = BookingService()

        ctk.CTkLabel(
            self,
            text="Booking Approvals",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

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
            command=self.approve_booking
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="Reject",
            fg_color="red",
            command=self.reject_booking
        ).pack(
            side="right",
            padx=5
        )

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

        for col in columns:

            self.table.heading(
                col,
                text=col
            )

            self.table.column(
                col,
                width=120,
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_bookings()

    def load_bookings(self):

        for row in self.table.get_children():

            self.table.delete(row)

        bookings = (
            self.service
            .get_pending_bookings()
        )

        for booking in bookings:

            self.table.insert(
                "",
                "end",
                values=booking
            )

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

    def approve_booking(self):

        booking = (
            self.get_selected_booking()
        )

        if not booking:

            return

        booking_id = booking[0]

        self.service.approve_booking(
            booking_id,
            self.user[0]
        )

        CTkMessagebox(
            title="Booking Approved",
            message="The booking has been approved.",
            icon="check"
        )

        self.load_bookings()

    def reject_booking(self):

        booking = (
            self.get_selected_booking()
        )

        if not booking:

            return

        booking_id = booking[0]

        self.service.reject_booking(
            booking_id,
            self.user[0]
        )

        CTkMessagebox(
            title="Booking Rejected",
            message="The booking has been rejected.",
            icon="warning"
        )

        self.load_bookings()