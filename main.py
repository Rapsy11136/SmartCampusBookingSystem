import customtkinter as ctk

from database.create_tables import create_tables
from database.seed import seed_database

from gui.login import LoginFrame
from gui.register import RegisterFrame
from gui.dashboard import DashboardFrame


class SmartCampusApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        create_tables()
        seed_database()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Smart Campus Resource Booking System")
        self.geometry("1200x700")
        self.minsize(1000, 650)

        self.current_frame = None
        self.current_user = None

        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_frame()
        self.current_frame = RegisterFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self, user):
        self.current_user = user

        self.clear_frame()

        self.current_frame = DashboardFrame(
            self,
            user
        )

        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = SmartCampusApp()
    app.mainloop()