import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master, width=220, corner_radius=0)

        self.master = master
        self.user = user

        self.pack(side="left", fill="y")
        self.pack_propagate(False)

        role = str(user[4]).lower()

        ctk.CTkLabel(
            self,
            text="Smart Campus",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self,
            text=user[1],
            font=("Arial", 14)
        ).pack()

        ctk.CTkLabel(
            self,
            text=user[4],
            font=("Arial", 12)
        ).pack(pady=(0, 25))

        # Dashboard (Everyone)
        self.add_button("🏠 Dashboard", self.master.show_home)

        # Lecturer
        if role == "lecturer":

            print("Creating Make Booking button")
            self.add_button("📅 Make Booking", self.master.show_make_booking)

            print("Creating My Bookings button")
            self.add_button("📖 My Bookings", self.master.show_my_bookings)

            print("Lecturer buttons created")

        # Campus Administrator
        elif role == "campus administrator":

            self.add_button("📚 Resources", self.master.show_resources)
            self.add_button("📅 Bookings", self.master.show_bookings)
            self.add_button("✅ Approvals", self.master.show_approvals)
            self.add_button("📊 Reports", self.master.show_reports)

        # System Operator
        elif role == "system operator":

            self.add_button("🏫 Campuses", self.master.show_campuses)
            self.add_button("👥 Users", self.master.show_users)
            self.add_button("📈 System Reports", self.master.show_reports)
            self.add_button("✅ Approvals", self.master.show_approvals)

        ctk.CTkButton(
            self,
            text="🚪 Logout",
            fg_color="red",
            hover_color="#B22222",
            command=self.master.logout
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    def add_button(self, text, command):

        ctk.CTkButton(
            self,
            text=text,
            command=command
        ).pack(fill="x", padx=15, pady=5)

