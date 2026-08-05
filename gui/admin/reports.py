import customtkinter as ctk
from tkinter import ttk

from services.report_service import ReportService


class ReportsFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.service = ReportService()

        ctk.CTkLabel(
            self,
            text="Reports",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        cards = ctk.CTkFrame(self)
        cards.pack(fill="x", padx=20)

        self.total_lbl = ctk.CTkLabel(cards, text="")
        self.total_lbl.pack(side="left", padx=20, pady=20)

        self.pending_lbl = ctk.CTkLabel(cards, text="")
        self.pending_lbl.pack(side="left", padx=20)

        self.approved_lbl = ctk.CTkLabel(cards, text="")
        self.approved_lbl.pack(side="left", padx=20)

        self.rejected_lbl = ctk.CTkLabel(cards, text="")
        self.rejected_lbl.pack(side="left", padx=20)

        columns = (
            "ID",
            "Lecturer",
            "Campus",
            "Resource",
            "Date",
            "Status"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=16
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=140)

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_report()

    def load_report(self):

        stats = self.service.get_statistics()

        self.total_lbl.configure(
            text=f"Total: {stats['total']}"
        )

        self.pending_lbl.configure(
            text=f"Pending: {stats['pending']}"
        )

        self.approved_lbl.configure(
            text=f"Approved: {stats['approved']}"
        )

        self.rejected_lbl.configure(
            text=f"Rejected: {stats['rejected']}"
        )

        for row in self.table.get_children():
            self.table.delete(row)

        for booking in self.service.get_all_bookings():
            self.table.insert("", "end", values=booking)