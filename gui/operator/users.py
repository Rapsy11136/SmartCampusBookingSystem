import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

from db_manager import Database


class UserFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user
        self.db = Database()

        # ==============================
        # TITLE
        # ==============================

        ctk.CTkLabel(
            self,
            text="User Management",
            font=("Arial", 28, "bold")
        ).pack(pady=(20, 10))

        # ==============================
        # TOOLBAR
        # ==============================

        toolbar = ctk.CTkFrame(self)
        toolbar.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            toolbar,
            width=300,
            placeholder_text="Search name or email..."
        )

        self.search_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        ctk.CTkButton(
            toolbar,
            text="Search",
            command=self.search_users
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.load_users
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="Delete User",
            fg_color="red",
            hover_color="#B22222",
            command=self.delete_user
        ).pack(
            side="right",
            padx=5
        )

        # ==============================
        # TABLE
        # ==============================

        columns = (
            "ID",
            "Full Name",
            "Email",
            "Role",
            "Campus"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        widths = {
            "ID": 60,
            "Full Name": 180,
            "Email": 220,
            "Role": 180,
            "Campus": 150
        }

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.load_users()

    # ==============================
    # LOAD USERS
    # ==============================

    def load_users(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.refresh_table()

    # ==============================
    # SEARCH
    # ==============================

    def search_users(self):

        keyword = self.search_entry.get().strip()

        self.refresh_table(keyword)

    # ==============================
    # REFRESH TABLE
    # ==============================

    def refresh_table(self, keyword=""):

        for item in self.table.get_children():
            self.table.delete(item)

        keyword = f"%{keyword}%"

        users = self.db.fetchall("""
            SELECT
                users.id,
                users.fullname,
                users.email,
                users.role,
                COALESCE(campuses.name, 'Not Assigned')

            FROM users

            LEFT JOIN campuses
                ON users.campus_id = campuses.id

            WHERE
                users.fullname LIKE ?
                OR users.email LIKE ?
                OR users.role LIKE ?
                OR COALESCE(campuses.name, '') LIKE ?

            ORDER BY users.fullname
        """, (
            keyword,
            keyword,
            keyword,
            keyword
        ))

        for user in users:

            self.table.insert(
                "",
                "end",
                values=user
            )

    # ==============================
    # DELETE USER
    # ==============================

    def delete_user(self):

        selected = self.table.selection()

        if not selected:

            CTkMessagebox(
                title="No Selection",
                message="Please select a user.",
                icon="warning"
            )

            return

        values = self.table.item(
            selected[0]
        )["values"]

        user_id = values[0]

        # Prevent deleting yourself

        if user_id == self.user[0]:

            CTkMessagebox(
                title="Not Allowed",
                message="You cannot delete your own account.",
                icon="warning"
            )

            return

        self.db.execute("""
            DELETE FROM users
            WHERE id=?
        """, (user_id,))

        self.refresh_table()

        CTkMessagebox(
            title="Success",
            message="User deleted successfully.",
            icon="check"
        )