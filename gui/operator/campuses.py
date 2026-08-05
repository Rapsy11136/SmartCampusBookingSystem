import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from gui.operator.campus_form import CampusForm

from services.campus_service import CampusService


class CampusesFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.service = CampusService()

        ctk.CTkLabel(
            self,
            text="Campus Management",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=20)

        self.search = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search Campus..."
        )
        self.search.pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Search",
            command=self.search_campuses
        ).pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.load_campuses
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Add",
            command=self.add_campus
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Edit",
            command=self.edit_campus
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Delete",
            fg_color="red",
            command=self.delete_campus
        ).pack(side="right", padx=5)

        columns = (
            "ID",
            "Campus",
            "Max Hours",
            "Open",
            "Close"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=180, anchor="center")

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_campuses()

    def load_campuses(self):

        for row in self.table.get_children():
            self.table.delete(row)

        for campus in self.service.get_campuses():
            self.table.insert("", "end", values=campus)

    def search_campuses(self):

        for row in self.table.get_children():
            self.table.delete(row)

        for campus in self.service.search_campuses(
            self.search.get()
        ):
            self.table.insert("", "end", values=campus)

    def add_campus(self):

        CampusForm(
            self,
            self.load_campuses
        )

    def edit_campus(self):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(selected[0])["values"]

        CampusForm(
            self,
            self.load_campuses,
            values
        )

    def delete_campus(self):

        selected = self.table.selection()

        if not selected:
            return

        campus = self.table.item(selected[0])["values"]

        self.service.delete_campus(campus[0])

        self.load_campuses()

        CTkMessagebox(
            title="Success",
            message="Campus deleted."
        )