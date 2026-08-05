from services.auth_service import AuthService
import customtkinter as ctk


class RegisterFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self,
            text="Create Account",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=25)

        card = ctk.CTkFrame(self, width=450)
        card.pack(pady=20)
        card.pack_propagate(False)
        card.configure(height=500)

        self.fullname = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Full Name"
        )
        self.fullname.pack(pady=(30, 10))

        self.email = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Email"
        )
        self.email.pack(pady=10)

        self.password = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.role = ctk.CTkOptionMenu(
            card,
            values=[
                "Lecturer",
                "Campus Administrator",
                "System Operator"
            ],
            width=340
        )
        self.role.pack(pady=15)

        self.message = ctk.CTkLabel(
            card,
            text="",
            text_color="red"
        )
        self.message.pack()

        self.register_button = ctk.CTkButton(
            card,
            text="Register",
            width=340,
            command=self.register
        )
        self.register_button.pack(pady=15)
        self.back_button = ctk.CTkButton(
            card,
            text="Back to Login",
            width=340,
            fg_color="gray30",
            command=self.back_to_login
        )
        self.back_button.pack()

        # Authentication service
        self.auth = AuthService()

    def back_to_login(self):
        self.master.show_login()

    def register(self):

        success, message = self.auth.register(
            self.fullname.get(),
            self.email.get(),
            self.password.get(),
            self.role.get()
        )

        if success:

            self.message.configure(
                text=message,
                text_color="green"
            )

            self.after(
                1200,
                self.master.show_login
            )

        else:

            self.message.configure(
                text=message,
                text_color="red")

