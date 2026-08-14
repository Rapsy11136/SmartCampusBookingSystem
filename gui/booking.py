import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from datetime import datetime

from services.booking_service import BookingService


# =========================================================
# BOOKING TIME RULES
# =========================================================

START_TIME_SLOTS = [
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00"
]

END_TIME_SLOTS = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00"
]


class BookingFrame(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(master)

        self.user = user
        self.service = BookingService()

        # =====================================================
        # TITLE
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="Make a Booking",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=(12, 5)
        )

        # =====================================================
        # BOOKING RULES
        # =====================================================

        rules_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        rules_frame.pack(
            fill="x",
            padx=35,
            pady=(5, 10)
        )

        ctk.CTkLabel(
            rules_frame,
            text="Booking Rules",
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(8, 3)
        )

        rules_text = (
            "• No bookings are allowed on Saturdays or Sundays.\n"
            "• Bookings must be made between 07:00 and 14:00.\n"
            "• A lecturer can make a maximum of 2 bookings per day.\n"
            "• Start time must be earlier than end time.\n"
            "• A resource cannot be booked by two people at the same time.\n"
            "• The booking date cannot be in the past.\n"
            "• A booking purpose is required."
        )

        ctk.CTkLabel(
            rules_frame,
            text=rules_text,
            justify="left",
            anchor="w",
            font=("Arial", 12)
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 8)
        )

        # =====================================================
        # FORM
        # =====================================================

        form = ctk.CTkFrame(
            self,
            width=320
        )

        form.pack(
            pady=5
        )

        # =====================================================
        # RESOURCE
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Resource"
        ).pack(
            pady=(5, 3)
        )

        resources = self.service.get_resources()

        self.resource_map = {
            r[1]: r[0]
            for r in resources
        }

        resource_names = list(
            self.resource_map.keys()
        )

        self.resource_menu = ctk.CTkOptionMenu(
            form,
            values=(
                resource_names
                if resource_names
                else ["No Resources"]
            ),
            width=300
        )

        self.resource_menu.pack(
            pady=3
        )

        # =====================================================
        # BOOKING DATE
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Booking Date"
        ).pack(
            pady=(5, 2)
        )

        self.date_entry = DateEntry(
            form,
            width=18,
            background="#1f6aa5",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )

        self.date_entry.pack(
            pady=2
        )

        # =====================================================
        # START TIME
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Start Time"
        ).pack(
            pady=(5, 2)
        )

        self.start_time = ctk.CTkOptionMenu(
            form,
            values=START_TIME_SLOTS,
            width=300
        )

        self.start_time.pack(
            pady=2
        )

        # =====================================================
        # END TIME
        # =====================================================

        ctk.CTkLabel(
            form,
            text="End Time"
        ).pack(
            pady=(5, 2)
        )

        self.end_time = ctk.CTkOptionMenu(
            form,
            values=END_TIME_SLOTS,
            width=300
        )

        self.end_time.pack(
            pady=2
        )

        # =====================================================
        # PURPOSE
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Purpose"
        ).pack(
            pady=(5, 2)
        )

        self.purpose = ctk.CTkTextbox(
            form,
            width=300,
            height=65
        )

        self.purpose.pack(
            pady=2
        )

        # =====================================================
        # SUBMIT BUTTON
        # =====================================================

        self.submit_button = ctk.CTkButton(
            form,
            text="Submit Booking",
            width=300,
            height=38,
            command=self.submit_booking
        )

        self.submit_button.pack(
            pady=(10, 10)
        )

    # =========================================================
    # SUBMIT BOOKING
    # =========================================================

    def submit_booking(self):

        try:

            print("========== BOOKING ==========")

            # -------------------------------------------------
            # RESOURCE
            # -------------------------------------------------

            resource_name = self.resource_menu.get()

            if resource_name not in self.resource_map:

                CTkMessagebox(
                    title="Booking Error",
                    message="Please select a valid resource.",
                    icon="warning"
                )

                return

            # -------------------------------------------------
            # USER
            # -------------------------------------------------

            lecturer_id = self.user[0]

            # -------------------------------------------------
            # RESOURCE ID
            # -------------------------------------------------

            resource_id = self.resource_map[
                resource_name
            ]

            # -------------------------------------------------
            # DATE
            # -------------------------------------------------

            booking_date = self.date_entry.get()

            selected_date = datetime.strptime(
                booking_date,
                "%Y-%m-%d"
            ).date()

            today = datetime.now().date()

            # -------------------------------------------------
            # PAST DATE
            # -------------------------------------------------

            if selected_date < today:

                CTkMessagebox(
                    title="Invalid Date",
                    message=(
                        "You cannot make a booking "
                        "for a past date."
                    ),
                    icon="warning"
                )

                return

            # -------------------------------------------------
            # WEEKEND
            # -------------------------------------------------

            if selected_date.weekday() >= 5:

                CTkMessagebox(
                    title="Weekend Booking",
                    message=(
                        "Bookings are not allowed on weekends.\n\n"
                        "Please select a Monday to Friday."
                    ),
                    icon="warning"
                )

                return

            # -------------------------------------------------
            # TIMES
            # -------------------------------------------------

            start_time = self.start_time.get()
            end_time = self.end_time.get()

            start = datetime.strptime(
                start_time,
                "%H:%M"
            )

            end = datetime.strptime(
                end_time,
                "%H:%M"
            )

            # -------------------------------------------------
            # START MUST BE BEFORE END
            # -------------------------------------------------

            if start >= end:

                CTkMessagebox(
                    title="Invalid Time",
                    message=(
                        "Start time must be earlier "
                        "than end time."
                    ),
                    icon="warning"
                )

                return

            # -------------------------------------------------
            # 14:00 CUTOFF
            # -------------------------------------------------

            cutoff = datetime.strptime(
                "14:00",
                "%H:%M"
            )

            if end > cutoff:

                CTkMessagebox(
                    title="Booking Time Restriction",
                    message=(
                        "Bookings cannot continue after 14:00.\n\n"
                        "Please select an end time of 14:00 or earlier."
                    ),
                    icon="warning"
                )

                return

            # -------------------------------------------------
            # PURPOSE
            # -------------------------------------------------

            purpose = self.purpose.get(
                "1.0",
                "end"
            ).strip()

            if not purpose:

                CTkMessagebox(
                    title="Missing Purpose",
                    message="Please enter the purpose of the booking.",
                    icon="warning"
                )

                return

            # -------------------------------------------------
            # CREATE BOOKING
            # -------------------------------------------------

            success, message = self.service.create_booking(
                lecturer_id,
                resource_id,
                booking_date,
                start_time,
                end_time,
                purpose
            )

            # -------------------------------------------------
            # RESULT
            # -------------------------------------------------

            CTkMessagebox(
                title="Booking Result",
                message=message,
                icon="check" if success else "warning"
            )

            if success:

                self.purpose.delete(
                    "1.0",
                    "end"
                )

        except ValueError:

            CTkMessagebox(
                title="Invalid Input",
                message="Please enter valid booking information.",
                icon="warning"
            )

        except Exception as e:

            print("BOOKING EXCEPTION:", e)

            CTkMessagebox(
                title="System Error",
                message=str(e),
                icon="cancel"
            )