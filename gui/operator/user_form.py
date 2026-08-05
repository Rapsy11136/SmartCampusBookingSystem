import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from services.user_service import UserService


class UserForm(ctk.CTkToplevel):

    def __init__(self, master, refresh_callback, user_data=None):
        super().__init__(master)

        self.service = UserService()
        self.refresh = refresh_callback
        self.user_data = user_data

        self.title("User")

        self.geometry("450x420")

        ctk.CTkLabel(
            self,
            text="User Details",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.fullname = ctk.CTkEntry(
            self,
            placeholder_text="Full Name",
            width=300
        )
        self.fullname.pack(pady=10)

        self.email = ctk.CTkEntry(
            self,
            placeholder_text="Email",
            width=300
        )
        self.email.pack(pady=10)

        self.password = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*",
            width=300
        )
        self.password.pack(pady=10)

        self.role = ctk.CTkOptionMenu(
            self,
            values=[
                "Lecturer",
                "Campus Administrator",
                "System Operator"
            ],
            width=300
        )
        self.role.pack(pady=10)

        if user_data:

            self.fullname.insert(0, user_data[1])
            self.email.insert(0, user_data[2])
            self.role.set(user_data[3])

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(pady=25)

    def save(self):

        if self.user_data is None:

            self.service.add_user(
                self.fullname.get(),
                self.email.get(),
                self.password.get(),
                self.role.get()
            )

        else:

            self.service.update_user(
                self.user_data[0],
                self.fullname.get(),
                self.email.get(),
                self.role.get()
            )

        self.refresh()

        CTkMessagebox(
            title="Success",
            message="User saved successfully.",
            icon="check"
        )

        self.destroy()