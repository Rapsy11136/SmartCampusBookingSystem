import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from gui.operator.user_form import UserForm

from services.user_service import UserService


class UsersFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.service = UserService()

        title = ctk.CTkLabel(
            self,
            text="User Management",
            font=("Arial",28,"bold")
        )
        title.pack(pady=20)

        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=20)

        self.search = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search User..."
        )
        self.search.pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Search",
            command=self.search_users
        ).pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.load_users
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Add",
            command=self.add_user
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Edit",
            command=self.edit_user
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Delete",
            fg_color="red",
            command=self.delete_user
        ).pack(side="right", padx=5)

        columns=(
            "ID",
            "Full Name",
            "Email",
            "Role"
        )

        self.table=ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:
            self.table.heading(col,text=col)
            self.table.column(col,width=220)

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_users()

    def load_users(self):

        for row in self.table.get_children():
            self.table.delete(row)

        users=self.service.get_users()

        for user in users:
            self.table.insert("", "end", values=user)

    def search_users(self):

        keyword=self.search.get()

        for row in self.table.get_children():
            self.table.delete(row)

        users=self.service.search_users(keyword)

        for user in users:
            self.table.insert("", "end", values=user)

    def add_user(self):

        UserForm(
            self,
            self.load_users
        )

    def edit_user(self):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(selected[0])["values"]

        UserForm(
            self,
            self.load_users,
            values
        )

    def delete_user(self):

        selected=self.table.selection()

        if not selected:
            return

        values=self.table.item(selected[0])["values"]

        self.service.delete_user(values[0])

        self.load_users()

        CTkMessagebox(
            title="Success",
            message="User deleted."
        )