import customtkinter as ctk

from gui.sidebar import Sidebar
from gui.dashboard_home import DashboardHome
from gui.resources import ResourceFrame
from services.resource_service import ResourceService
from gui.booking import BookingFrame
from gui.lecturer.my_bookings import MyBookingsFrame
from gui.booking import BookingFrame
from gui.admin.approvals import ApprovalFrame


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.master = master
        self.user = user

        self.pack(fill="both", expand=True)

        # Sidebar
        Sidebar(self, self.user)

        # Content area
        self.content = ctk.CTkFrame(self)
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Resource service instance
        self.resource_service = ResourceService()

        # Show home by default
        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        # Fetch live resource stats
        total = self.resource_service.total_resources()
        available = self.resource_service.available_resources()
        booked = self.resource_service.booked_resources()

        # Pass stats into DashboardHome
        page = DashboardHome(
            self.content,
            self.user,
            total=total,
            available=available,
            booked=booked
        )
        page.pack(fill="both", expand=True)

    def show_resources(self):
        self.clear_content()
        page = ResourceFrame(self.content)
        page.pack(fill="both", expand=True)

    def show_bookings(self):
        self.clear_content()

        page = BookingFrame(
            self.content,
            self.user
        )

        page.pack(fill="both", expand=True)

    def show_campuses(self):
        self.clear_content()
        ctk.CTkLabel(
            self.content,
            text="Campus Module",
            font=("Arial", 28)
        ).pack(pady=50)

    def show_reports(self):
        self.clear_content()
        ctk.CTkLabel(
            self.content,
            text="Reports Module",
            font=("Arial", 28)
        ).pack(pady=50)

    def show_approvals(self):
        print("APPROVAL BUTTON CLICKED")

        self.clear_content()

        import customtkinter as ctk

        ctk.CTkLabel(
            self.content,
            text="APPROVAL PAGE",
            font=("Arial", 30)
        ).pack(pady=100)

    def show_users(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="User Management",
            font=("Arial", 28)
        ).pack(pady=50)

    def logout(self):
        self.master.show_login()

    def show_make_booking(self):
        self.clear_content()

        page = BookingFrame(
            self.content,
            self.user
        )

        page.pack(fill="both", expand=True)