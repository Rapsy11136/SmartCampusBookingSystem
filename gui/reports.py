import customtkinter as ctk
from tkinter import ttk

from db_manager import Database


class ReportsFrame(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(master)

        self.user = user
        self.db = Database()

        self.role = str(
            user[4]
        ).lower()

        self.campus_id = user[5]

        # ==============================
        # TITLE
        # ==============================

        ctk.CTkLabel(
            self,
            text="Reports & Management Information",
            font=("Arial", 28, "bold")
        ).pack(
            pady=(20, 5)
        )

        # ==============================
        # DESCRIPTION
        # ==============================

        ctk.CTkLabel(
            self,
            text=(
                "Monitor bookings, resource usage and "
                "campus performance."
            ),
            font=("Arial", 14)
        ).pack(
            pady=(0, 15)
        )

        # ==============================
        # SUMMARY CARDS
        # ==============================

        self.cards = ctk.CTkFrame(self)

        self.cards.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.total_bookings_label = self.create_card(
            self.cards,
            "Total Bookings",
            "0"
        )

        self.total_resources_label = self.create_card(
            self.cards,
            "Resources",
            "0"
        )

        self.available_label = self.create_card(
            self.cards,
            "Available",
            "0"
        )

        self.avg_duration_label = self.create_card(
            self.cards,
            "Avg Duration",
            "0 hrs"
        )

        # ==============================
        # REFRESH
        # ==============================

        ctk.CTkButton(
            self,
            text="Refresh Reports",
            command=self.load_reports
        ).pack(
            pady=10
        )

        # ==============================
        # CAMPUS TABLE
        # ==============================

        ctk.CTkLabel(
            self,
            text="Campus Usage Report",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(10, 5)
        )

        columns = (
            "Campus",
            "Bookings",
            "Resources",
            "Available",
            "Approved",
            "Pending"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=130,
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        self.load_reports()

    # ==============================
    # CARD
    # ==============================

    def create_card(
            self,
            parent,
            title,
            value
    ):

        card = ctk.CTkFrame(
            parent,
            width=180,
            height=100
        )

        card.pack(
            side="left",
            padx=10,
            pady=10
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14)
        ).pack(
            pady=(15, 5)
        )

        label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 25, "bold")
        )

        label.pack()

        return label

    # ==============================
    # LOAD REPORTS
    # ==============================

    def load_reports(self):

        for item in self.table.get_children():
            self.table.delete(item)

        # ==============================
        # CAMPUS ADMIN
        # ==============================

        if self.role == "campus administrator":

            campus_filter = """
                WHERE c.id=?
            """

            params = (
                self.campus_id,
            )

        # ==============================
        # SYSTEM OPERATOR
        # ==============================

        else:

            campus_filter = ""

            params = ()

        # ==============================
        # SUMMARY
        # ==============================

        total_bookings = self.db.fetchone(f"""
            SELECT COUNT(*)
            FROM bookings b
            JOIN resources r
                ON b.resource_id = r.id
            JOIN campuses c
                ON r.campus_id = c.id
            {campus_filter}
        """, params)[0]

        total_resources = self.db.fetchone(f"""
            SELECT COUNT(*)
            FROM resources r
            JOIN campuses c
                ON r.campus_id = c.id
            {campus_filter}
        """, params)[0]

        available = self.db.fetchone(f"""
            SELECT COUNT(*)
            FROM resources r
            JOIN campuses c
                ON r.campus_id = c.id
            WHERE r.status='Available'
            {"AND c.id=?" if self.role == "campus administrator" else ""}
        """, (
            self.campus_id,
        ) if self.role == "campus administrator" else ())[0]

        # ==============================
        # AVERAGE DURATION
        # ==============================

        duration_where = ""

        if self.role == "campus administrator":

            duration_where = """
                AND r.campus_id=?
            """

        avg_duration = self.db.fetchone(f"""
            SELECT AVG(
                (
                    CAST(substr(b.end_time, 1, 2) AS INTEGER) * 60
                    + CAST(substr(b.end_time, 4, 2) AS INTEGER)
                )
                -
                (
                    CAST(substr(b.start_time, 1, 2) AS INTEGER) * 60
                    + CAST(substr(b.start_time, 4, 2) AS INTEGER)
                )
            )
            FROM bookings b
            JOIN resources r
                ON b.resource_id = r.id
            WHERE b.status!='Cancelled'
            {duration_where}
        """, (
            self.campus_id,
        ) if self.role == "campus administrator" else ())[0]

        if avg_duration is None:
            avg_duration = 0

        avg_hours = round(
            avg_duration / 60,
            2
        )

        # ==============================
        # UPDATE CARDS
        # ==============================

        self.total_bookings_label.configure(
            text=str(total_bookings)
        )

        self.total_resources_label.configure(
            text=str(total_resources)
        )

        self.available_label.configure(
            text=str(available)
        )

        self.avg_duration_label.configure(
            text=f"{avg_hours} hrs"
        )

        # ==============================
        # CAMPUS REPORT
        # ==============================

        campuses = self.db.fetchall(f"""
            SELECT
                c.name,

                (
                    SELECT COUNT(*)
                    FROM bookings b
                    JOIN resources r
                        ON b.resource_id=r.id
                    WHERE r.campus_id=c.id
                ),

                (
                    SELECT COUNT(*)
                    FROM resources r
                    WHERE r.campus_id=c.id
                ),

                (
                    SELECT COUNT(*)
                    FROM resources r
                    WHERE
                        r.campus_id=c.id
                        AND r.status='Available'
                ),

                (
                    SELECT COUNT(*)
                    FROM bookings b
                    JOIN resources r
                        ON b.resource_id=r.id
                    WHERE
                        r.campus_id=c.id
                        AND b.status='Approved'
                ),

                (
                    SELECT COUNT(*)
                    FROM bookings b
                    JOIN resources r
                        ON b.resource_id=r.id
                    WHERE
                        r.campus_id=c.id
                        AND b.status='Pending'
                )

            FROM campuses c

            { "WHERE c.id=?" if self.role == "campus administrator" else "" }

            ORDER BY c.name
        """, (
            self.campus_id,
        ) if self.role == "campus administrator" else ())

        for row in campuses:

            self.table.insert(
                "",
                "end",
                values=row
            )