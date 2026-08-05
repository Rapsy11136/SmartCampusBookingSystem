import customtkinter as ctk

from services.auth_service import AuthService


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.auth = AuthService()

        self.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self,
            text="Smart Campus Resource Booking System",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Login to continue",
            font=("Arial", 16)
        )
        subtitle.pack(pady=(0, 30))

        card = ctk.CTkFrame(self, width=420, height=360)
        card.pack()
        card.pack_propagate(False)

        self.email_entry = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Email"
        )
        self.email_entry.pack(pady=(40, 15))

        self.password_entry = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Password",
            show="*"
        )
        self.password_entry.pack(pady=10)

        self.message = ctk.CTkLabel(
            card,
            text="",
            text_color="red"
        )
        self.message.pack(pady=10)

        ctk.CTkButton(
            card,
            text="Login",
            width=340,
            command=self.login
        ).pack(pady=10)

        ctk.CTkButton(
            card,
            text="Create Account",
            width=340,
            fg_color="gray30",
            command=self.master.show_register
        ).pack()

    def login(self):

        success, result = self.auth.login(
            self.email_entry.get(),
            self.password_entry.get()
        )

        if success:

            self.master.show_dashboard(result)

        else:

            self.message.configure(
                text=result
            )