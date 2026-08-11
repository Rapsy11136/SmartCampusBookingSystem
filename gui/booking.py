import customtkinter as ctk

from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry

from services.booking_service import BookingService


TIME_SLOTS = [
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00"
]


class BookingFrame(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(master)

        self.user = user
        self.service = BookingService()

        # -----------------------------------------
        # TITLE
        # -----------------------------------------

        ctk.CTkLabel(
            self,
            text="Make a Booking",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        # -----------------------------------------
        # FORM
        # -----------------------------------------

        form = ctk.CTkFrame(self)
        form.pack(pady=10)

        # -----------------------------------------
        # CAMPUS
        # -----------------------------------------

        ctk.CTkLabel(
            form,
            text="Campus"
        ).pack(pady=(10, 5))

        campuses = self.service.get_campuses()

        self.campus_map = {
            campus[1]: campus[0]
            for campus in campuses
        }

        campus_names = list(self.campus_map.keys())

        self.campus_menu = ctk.CTkOptionMenu(
            form,
            values=campus_names if campus_names else ["No Campuses"],
            command=self.load_resources
        )

        self.campus_menu.pack(pady=5)

        # -----------------------------------------
        # RESOURCE
        # -----------------------------------------

        ctk.CTkLabel(
            form,
            text="Resource"
        ).pack(pady=(10, 5))

        self.resource_map = {}

        self.resource_menu = ctk.CTkOptionMenu(
            form,
            values=["Select Campus First"]
        )

        self.resource_menu.pack(pady=5)

        # -----------------------------------------
        # DATE
        # -----------------------------------------

        ctk.CTkLabel(
            form,
            text="Booking Date"
        ).pack(pady=(10, 5))

        self.date_entry = DateEntry(
            form,
            width=18,
            background="#1f6aa5",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )

        self.date_entry.pack(pady=5)

        # -----------------------------------------
        # START TIME
        # -----------------------------------------

        ctk.CTkLabel(
            form,
            text="Start Time"
        ).pack(pady=(10, 5))

        self.start_time = ctk.CTkOptionMenu(
            form,
            values=TIME_SLOTS
        )

        self.start_time.pack(pady=5)

        # -----------------------------------------
        # END TIME
        # -----------------------------------------

        ctk.CTkLabel(
            form,
            text="End Time"
        ).pack(pady=(10, 5))

        self.end_time = ctk.CTkOptionMenu(
            form,
            values=TIME_SLOTS
        )

        self.end_time.pack(pady=5)

        # -----------------------------------------
        # PURPOSE
        # -----------------------------------------

        ctk.CTkLabel(
            form,
            text="Booking Purpose"
        ).pack(pady=(10, 5))

        self.purpose = ctk.CTkTextbox(
            form,
            width=350,
            height=100
        )

        self.purpose.pack(pady=5)

        # -----------------------------------------
        # SUBMIT
        # -----------------------------------------

        ctk.CTkButton(
            form,
            text="Submit Booking",
            command=self.submit_booking
        ).pack(pady=20)

        campus_name = "Unknown"

        for campus in self.service.db.fetchall(
                "SELECT id, name FROM campuses"
        ):
            if campus[0] == self.user[5]:
                campus_name = campus[1]
                break

        ctk.CTkLabel(
            self,
            text=f"Campus: {campus_name}",
            font=("Arial", 16)
        ).pack(pady=(0, 15))

        # -----------------------------------------
        # LOAD LECTURER CAMPUS
        # -----------------------------------------

        lecturer_campus_id = self.user[5]

        if lecturer_campus_id:

            for name, campus_id in self.campus_map.items():

                if campus_id == lecturer_campus_id:

                    self.campus_menu.set(name)

                    self.load_resources(name)

                    break

    # =================================================
    # LOAD RESOURCES
    # =================================================

    def load_resources(self, campus_name):

        if campus_name not in self.campus_map:
            return

        campus_id = self.campus_map[campus_name]

        # Make sure lecturer belongs to this campus
        lecturer_campus_id = self.user[5]

        if lecturer_campus_id != campus_id:

            self.resource_map = {}

            self.resource_menu.configure(
                values=["Not Your Campus"]
            )

            self.resource_menu.set(
                "Not Your Campus"
            )

            return

        campus_id = self.user[5]

        resources = self.service.get_resources(
            campus_id
        )

        self.resource_map = {
            resource[1]: resource[0]
            for resource in resources
        }

        resource_names = list(
            self.resource_map.keys()
        )

        if resource_names:

            self.resource_menu.configure(
                values=resource_names
            )

            self.resource_menu.set(
                resource_names[0]
            )

        else:

            self.resource_menu.configure(
                values=["No Resources Available"]
            )

            self.resource_menu.set(
                "No Resources Available"
            )

    # =================================================
    # SUBMIT BOOKING
    # =================================================

    def submit_booking(self):

        try:

            campus_name = self.campus_menu.get()

            if campus_name not in self.campus_map:

                CTkMessagebox(
                    title="Booking Error",
                    message="Please select a valid campus.",
                    icon="cancel"
                )

                return

            campus_id = self.campus_map[campus_name]

            resource_name = self.resource_menu.get()

            if resource_name not in self.resource_map:

                CTkMessagebox(
                    title="Booking Error",
                    message="Please select a valid resource.",
                    icon="cancel"
                )

                return

            resource_id = self.resource_map[
                resource_name
            ]

            booking_date = self.date_entry.get()

            start_time = self.start_time.get()

            end_time = self.end_time.get()

            purpose = self.purpose.get(
                "1.0",
                "end"
            ).strip()

            # -------------------------------------
            # CREATE BOOKING
            # -------------------------------------

            success, message = self.service.create_booking(

                lecturer_id=self.user[0],

                campus_id=campus_id,

                resource_id=resource_id,

                booking_date=booking_date,

                start_time=start_time,

                end_time=end_time,

                purpose=purpose
            )

            if success:

                CTkMessagebox(
                    title="Booking Successful",
                    message=message,
                    icon="check"
                )

                self.purpose.delete(
                    "1.0",
                    "end"
                )

            else:

                CTkMessagebox(
                    title="Booking Failed",
                    message=message,
                    icon="warning"
                )

        except Exception as e:

            print("BOOKING ERROR:", e)

            CTkMessagebox(
                title="System Error",
                message=str(e),
                icon="cancel"
            )