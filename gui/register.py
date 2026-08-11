import customtkinter as ctk

from services.auth_service import AuthService


class RegisterFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.auth = AuthService()

        self.pack(fill="both", expand=True)

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self,
            text="Create Account",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=25)

        # =========================
        # CARD
        # =========================

        card = ctk.CTkFrame(
            self,
            width=450,
            height=580
        )

        card.pack(pady=10)
        card.pack_propagate(False)

        # =========================
        # FULL NAME
        # =========================

        self.fullname = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Full Name"
        )
        self.fullname.pack(pady=(25, 10))

        # =========================
        # EMAIL
        # =========================

        self.email = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Email"
        )
        self.email.pack(pady=10)

        # =========================
        # PASSWORD
        # =========================

        self.password = ctk.CTkEntry(
            card,
            width=340,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        # =========================
        # ROLE
        # =========================

        role_label = ctk.CTkLabel(
            card,
            text="Select Role"
        )
        role_label.pack(pady=(15, 5))

        self.role = ctk.CTkOptionMenu(
            card,
            width=340,
            values=[
                "Lecturer",
                "Campus Administrator",
                "System Operator"
            ],
            command=self.role_changed
        )
        self.role.pack(pady=5)

        # =========================
        # CAMPUS
        # =========================

        self.campus_label = ctk.CTkLabel(
            card,
            text="Select Campus"
        )
        self.campus_label.pack(pady=(15, 5))

        self.campuses = self.auth.get_campuses()

        self.campus_map = {
            campus[1]: campus[0]
            for campus in self.campuses
        }

        campus_names = list(self.campus_map.keys())

        if campus_names:

            self.campus = ctk.CTkOptionMenu(
                card,
                width=340,
                values=campus_names
            )

            self.campus.pack(pady=5)

        else:

            self.campus = None

            self.campus_label.configure(
                text="No campuses available"
            )

        # =========================
        # MESSAGE
        # =========================

        self.message = ctk.CTkLabel(
            card,
            text="",
            text_color="red",
            wraplength=340
        )
        self.message.pack(pady=10)

        # =========================
        # REGISTER BUTTON
        # =========================

        self.register_button = ctk.CTkButton(
            card,
            text="Register",
            width=340,
            command=self.register
        )
        self.register_button.pack(pady=10)

        # =========================
        # BACK BUTTON
        # =========================

        self.back_button = ctk.CTkButton(
            card,
            text="Back to Login",
            width=340,
            fg_color="gray30",
            command=self.back_to_login
        )
        self.back_button.pack()

        # Check initial role
        self.role_changed(self.role.get())

    # ==========================================================
    # ROLE CHANGED
    # ==========================================================

    def role_changed(self, selected_role):

        if selected_role == "System Operator":

            # System operators do not need a campus
            if self.campus is not None:
                self.campus.configure(state="disabled")

            self.campus_label.configure(
                text="Campus: Not required"
            )

        else:

            if self.campus is not None:
                self.campus.configure(state="normal")

            self.campus_label.configure(
                text="Select Campus"
            )

    # ==========================================================
    # BACK TO LOGIN
    # ==========================================================

    def back_to_login(self):

        self.master.show_login()

    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(self):

        fullname = self.fullname.get().strip()
        email = self.email.get().strip()
        password = self.password.get()
        role = self.role.get()

        # =========================
        # VALIDATION
        # =========================

        if not fullname:

            self.show_message(
                "Full name is required.",
                "red"
            )
            return

        if not email:

            self.show_message(
                "Email is required.",
                "red"
            )
            return

        if "@" not in email or "." not in email:

            self.show_message(
                "Please enter a valid email address.",
                "red"
            )
            return

        if not password:

            self.show_message(
                "Password is required.",
                "red"
            )
            return

        if len(password) < 6:

            self.show_message(
                "Password must be at least 6 characters.",
                "red"
            )
            return

        # =========================
        # CAMPUS
        # =========================

        campus_id = None

        if role != "System Operator":

            if self.campus is None:

                self.show_message(
                    "No campus is available. Please add a campus first.",
                    "red"
                )
                return

            campus_name = self.campus.get()

            if campus_name not in self.campus_map:

                self.show_message(
                    "Please select a campus.",
                    "red"
                )
                return

            campus_id = self.campus_map[campus_name]

        # =========================
        # REGISTER
        # =========================

        success, message = self.auth.register(
            fullname,
            email,
            password,
            role,
            campus_id
        )

        if success:

            self.show_message(
                message,
                "green"
            )

            self.after(
                1200,
                self.master.show_login
            )

        else:

            self.show_message(
                message,
                "red"
            )

    # ==========================================================
    # MESSAGE
    # ==========================================================

    def show_message(self, message, colour):

        self.message.configure(
            text=message,
            text_color=colour
        )