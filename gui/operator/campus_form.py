import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from services.campus_service import CampusService


class CampusForm(ctk.CTkToplevel):

    def __init__(self, master, refresh_callback, campus_data=None):
        super().__init__(master)

        self.service = CampusService()
        self.refresh = refresh_callback
        self.campus_data = campus_data

        self.title("Campus")
        self.geometry("450x450")

        ctk.CTkLabel(
            self,
            text="Campus Details",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.name = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Campus Name"
        )
        self.name.pack(pady=10)

        self.duration = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Maximum Booking Hours"
        )
        self.duration.pack(pady=10)

        self.opening = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Opening Time (HH:MM)"
        )
        self.opening.pack(pady=10)

        self.closing = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Closing Time (HH:MM)"
        )
        self.closing.pack(pady=10)

        if campus_data:

            self.name.insert(0, campus_data[1])
            self.duration.insert(0, campus_data[2])
            self.opening.insert(0, campus_data[3])
            self.closing.insert(0, campus_data[4])

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(pady=25)

    def save(self):

        if self.campus_data is None:

            self.service.add_campus(
                self.name.get(),
                self.duration.get(),
                self.opening.get(),
                self.closing.get()
            )

        else:

            self.service.update_campus(
                self.campus_data[0],
                self.name.get(),
                self.duration.get(),
                self.opening.get(),
                self.closing.get()
            )

        self.refresh()

        CTkMessagebox(
            title="Success",
            message="Campus saved successfully.",
            icon="check"
        )

        self.destroy()