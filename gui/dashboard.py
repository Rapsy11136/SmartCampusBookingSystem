import customtkinter as ctk

from gui.sidebar import Sidebar
from gui.dashboard_home import DashboardHome
from gui.resources import ResourceFrame
from services.resource_service import ResourceService
from gui.booking import BookingFrame
from gui.lecturer.my_bookings import MyBookingsFrame
from gui.admin.approvals import ApprovalFrame
from gui.operator.campuses import CampusFrame
from gui.operator.users import UserFrame
from gui.reports import ReportsFrame


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.master = master
        self.user = user

        self.pack(fill="both", expand=True)

        # =========================
        # SIDEBAR
        # =========================
        Sidebar(self, self.user)

        # =========================
        # CONTENT AREA
        # =========================
        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =========================
        # SERVICES
        # =========================
        self.resource_service = ResourceService()

        # =========================
        # DEFAULT PAGE
        # =========================
        self.show_home()

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================================================
    # DASHBOARD HOME
    # =========================================================

    def show_home(self):

        self.clear_content()

        try:

            total = self.resource_service.total_resources()
            available = self.resource_service.available_resources()
            booked = self.resource_service.booked_resources()

        except Exception as e:

            print("Dashboard statistics error:", e)

            total = 0
            available = 0
            booked = 0

        page = DashboardHome(
            self.content,
            self.user,
            total=total,
            available=available,
            booked=booked
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # RESOURCES
    # =========================================================

    def show_resources(self):

        self.clear_content()

        page = ResourceFrame(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CAMPUS ADMIN BOOKINGS
    # =========================================================

    def show_bookings(self):

        self.clear_content()

        page = BookingFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # LECTURER - MAKE BOOKING
    # =========================================================

    def show_make_booking(self):

        self.clear_content()

        page = BookingFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # LECTURER - MY BOOKINGS
    # =========================================================

    def show_my_bookings(self):

        self.clear_content()

        page = MyBookingsFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CAMPUS ADMIN - APPROVALS
    # =========================================================

    def show_approvals(self):

        self.clear_content()

        page = ApprovalFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CAMPUSES
    # =========================================================

    def show_campuses(self):

        self.clear_content()

        page = CampusFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # USERS
    # =========================================================

    def show_users(self):

        self.clear_content()

        page = UserFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # REPORTS
    # =========================================================

    def show_reports(self):

        self.clear_content()

        page = ReportsFrame(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        self.master.show_login()