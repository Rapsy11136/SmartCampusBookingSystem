import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from services.resource_service import ResourceService

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

        title = ctk.CTkLabel(
            self,
            text="Make a Booking",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(self)
        form.pack(pady=20)

        resources = self.service.get_resources()

        self.resource_map = {
            r[1]: r[0]
            for r in resources
        }

        resource_names = list(self.resource_map.keys())

        self.resource_menu = ctk.CTkOptionMenu(
            form,
            values=resource_names if resource_names else ["No Resources"]
        )
        self.resource_menu.pack(pady=10)

        date_label = ctk.CTkLabel(
            form,
            text="Booking Date"
        )
        date_label.pack(pady=(10, 5))

        self.date_entry = DateEntry(
            form,
            width=18,
            background="#1f6aa5",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )
        self.date_entry.pack(pady=(0, 10))

        self.start_time = ctk.CTkOptionMenu(
            form,
            values=TIME_SLOTS
        )
        self.start_time.pack(pady=10)

        self.end_time = ctk.CTkOptionMenu(
            form,
            values=TIME_SLOTS
        )
        self.end_time.pack(pady=10)

        self.purpose = ctk.CTkTextbox(
            form,
            width=300,
            height=120
        )
        self.purpose.pack(pady=10)

        ctk.CTkButton(
            form,
            text="Submit Booking",
            command=self.submit_booking
        ).pack(pady=20)

    def submit_booking(self):

        try:

            print("========== BOOKING ==========")

            resource_name = self.resource_menu.get()
            print("Resource:", resource_name)

            if resource_name not in self.resource_map:
                CTkMessagebox(
                    title="Error",
                    message="No resource selected."
                )
                return

            lecturer_id = self.user[0]
            resource_id = self.resource_map[resource_name]
            booking_date = self.date_entry.get()
            start_time = self.start_time.get()
            end_time = self.end_time.get()
            purpose = self.purpose.get("1.0", "end").strip()

            print("Lecturer:", lecturer_id)
            print("Resource ID:", resource_id)
            print("Date:", booking_date)
            print("Start:", start_time)
            print("End:", end_time)
            print("Purpose:", purpose)

            success, message = self.service.create_booking(
                lecturer_id,
                resource_id,
                booking_date,
                start_time,
                end_time,
                purpose
            )

            print("Returned:", success, message)

            CTkMessagebox(
                title="Booking Result",
                message=message,
                icon="check" if success else "warning"
            )

        except Exception as e:

            print("EXCEPTION:", e)

            CTkMessagebox(
                title="Exception",
                message=str(e),
                icon="cancel"
            )

    def load_resources(self, campus_name):

        campus_id = self.campus_map[campus_name]

        resources = self.resource_service.get_resources_by_campus(
            campus_id
        )

        self.resource_map = {
            r[1]: r[0]
            for r in resources
        }

        names = list(self.resource_map.keys())

        if names:
            self.resource_menu.configure(values=names)
            self.resource_menu.set(names[0])
        else:
            self.resource_menu.configure(values=["No Resources"])
            self.resource_menu.set("No Resources")