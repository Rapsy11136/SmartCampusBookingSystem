import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

from db_manager import Database


class CampusFrame(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user
        self.db = Database()

        # ==============================
        # TITLE
        # ==============================

        ctk.CTkLabel(
            self,
            text="Campus Management",
            font=("Arial", 28, "bold")
        ).pack(pady=(20, 10))

        # ==============================
        # FORM
        # ==============================

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=25, pady=10)

        self.name_entry = ctk.CTkEntry(
            form,
            width=300,
            placeholder_text="Campus Name"
        )
        self.name_entry.pack(
            side="left",
            padx=10,
            pady=15
        )

        ctk.CTkButton(
            form,
            text="Add Campus",
            command=self.add_campus
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            form,
            text="Delete Campus",
            fg_color="red",
            hover_color="#B22222",
            command=self.delete_campus
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            form,
            text="Refresh",
            command=self.load_campuses
        ).pack(
            side="left",
            padx=5
        )

        # ==============================
        # TABLE
        # ==============================

        columns = (
            "ID",
            "Campus Name",
            "Resources",
            "Users",
            "Bookings"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=150,
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.load_campuses()

    # ==============================
    # LOAD CAMPUSES
    # ==============================

    def load_campuses(self):

        for item in self.table.get_children():
            self.table.delete(item)

        campuses = self.db.fetchall("""
            SELECT
                c.id,
                c.name,

                (
                    SELECT COUNT(*)
                    FROM resources r
                    WHERE r.campus_id = c.id
                ) AS resources,

                (
                    SELECT COUNT(*)
                    FROM users u
                    WHERE u.campus_id = c.id
                ) AS users,

                (
                    SELECT COUNT(*)
                    FROM bookings b
                    JOIN resources r2
                        ON b.resource_id = r2.id
                    WHERE r2.campus_id = c.id
                ) AS bookings

            FROM campuses c

            ORDER BY c.name
        """)

        for campus in campuses:

            self.table.insert(
                "",
                "end",
                values=campus
            )

    # ==============================
    # ADD CAMPUS
    # ==============================

    def add_campus(self):

        name = self.name_entry.get().strip()

        if not name:

            CTkMessagebox(
                title="Validation Error",
                message="Campus name is required.",
                icon="warning"
            )

            return

        existing = self.db.fetchone("""
            SELECT id
            FROM campuses
            WHERE LOWER(name)=LOWER(?)
        """, (name,))

        if existing:

            CTkMessagebox(
                title="Duplicate Campus",
                message="This campus already exists.",
                icon="warning"
            )

            return

        self.db.execute("""
            INSERT INTO campuses(name)
            VALUES(?)
        """, (name,))

        self.name_entry.delete(
            0,
            "end"
        )

        self.load_campuses()

        CTkMessagebox(
            title="Success",
            message="Campus added successfully.",
            icon="check"
        )

    # ==============================
    # DELETE CAMPUS
    # ==============================

    def delete_campus(self):

        selected = self.table.selection()

        if not selected:

            CTkMessagebox(
                title="No Selection",
                message="Please select a campus.",
                icon="warning"
            )

            return

        values = self.table.item(
            selected[0]
        )["values"]

        campus_id = values[0]

        resource_count = values[2]
        user_count = values[3]
        booking_count = values[4]

        if resource_count > 0:

            CTkMessagebox(
                title="Cannot Delete",
                message=(
                    "This campus has resources assigned to it.\n"
                    "Remove or reassign the resources first."
                ),
                icon="warning"
            )

            return

        if user_count > 0:

            CTkMessagebox(
                title="Cannot Delete",
                message=(
                    "This campus has users assigned to it.\n"
                    "Reassign the users first."
                ),
                icon="warning"
            )

            return

        if booking_count > 0:

            CTkMessagebox(
                title="Cannot Delete",
                message=(
                    "This campus has booking records and "
                    "cannot be deleted."
                ),
                icon="warning"
            )

            return

        self.db.execute("""
            DELETE FROM campuses
            WHERE id=?
        """, (campus_id,))

        self.load_campuses()

        CTkMessagebox(
            title="Success",
            message="Campus deleted successfully.",
            icon="check"
        )