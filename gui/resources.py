from CTkMessagebox import CTkMessagebox
from tkinter import ttk
import customtkinter as ctk
from services.resource_service import ResourceService


class ResourceFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.service = ResourceService()
        self.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            self,
            text="Resource Management",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        # Toolbar
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            width=250,
            placeholder_text="Search resources..."
        )
        self.search_entry.pack(side="left", padx=10)

        ctk.CTkButton(
            toolbar,
            text="Search",
            command=self.search_resources
        ).pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.load_resources
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            toolbar,
            text="Add Resource",
            command=self.open_add_dialog
        ).pack(side="right")

        ctk.CTkButton(
            toolbar,
            text="Delete Selected",
            command=self.delete_selected_resource
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            toolbar,
            text="Edit Selected",
            command=self.edit_selected_resource
        ).pack(side="right", padx=10)

        # Table

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "ID",
            "Campus",
            "Name",
            "Type",
            "Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=150)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_resources(self):

        resources = self.service.get_all_resources()

        self.display_resources(resources)

        if len(resources) == 0:
            self.table.insert("end", "No resources found.")
            return

        header = (
            f"{'ID':<5}"
            f"{'Campus':<20}"
            f"{'Name':<25}"
            f"{'Type':<20}"
            f"{'Status'}\n"
        )
        self.table.insert("end", header)
        self.table.insert("end", "-" * 90 + "\n")

        for row in resources:
            self.table.insert(
                "end",
                f"{row[0]:<5}"
                f"{row[1]:<20}"
                f"{row[2]:<25}"
                f"{row[3]:<20}"
                f"{row[4]}\n"
            )

    def delete_resource(self, resource_id):

        answer = CTkMessagebox(
            title="Delete Resource",
            message="Are you sure you want to delete this resource?",
            icon="question",
            option_1="Cancel",
            option_2="Delete"
        )

        if answer.get() == "Delete":
            self.service.delete_resource(resource_id)

            self.load_resources()

            CTkMessagebox(
                title="Success",
                message="Resource deleted successfully.",
                icon="check"
            )

    def delete_selected_resource(self):

        selected = self.table.selection()

        if not selected:
            CTkMessagebox(
                title="No Selection",
                message="Please select a resource to delete.",
                icon="warning"
            )
            return

        values = self.table.item(selected[0], "values")

        resource_id = values[0]

        self.delete_resource(resource_id)

    def edit_selected_resource(self):

        selected = self.table.selection()

        if not selected:
            CTkMessagebox(
                title="No Selection",
                message="Please select a resource.",
                icon="warning"
            )

            return

        values = self.table.item(selected[0], "values")

        resource_id = values[0]

        self.open_edit_dialog(resource_id)

    def search_resources(self):
        keyword = self.search_entry.get().strip()
        if keyword == "":
            self.load_resources()
            return

        resources = self.service.search_resources(keyword)
        self.display_resources(resources)

    def display_resources(self, resources):

        for row in self.table.get_children():
            self.table.delete(row)

        for resource in resources:
            self.table.insert(
                "",
                "end",
                values=resource
            )

        header = (
            f"{'ID':<5}"
            f"{'Campus':<20}"
            f"{'Name':<25}"
            f"{'Type':<20}"
            f"{'Status'}\n"
        )

        self.table.insert("end", header)
        self.table.insert("end", "-" * 90 + "\n")

        for row in resources:
            self.table.insert(
                "end",
                f"{row[0]:<5}"
                f"{row[1]:<20}"
                f"{row[2]:<25}"
                f"{row[3]:<20}"
                f"{row[4]}\n"
            )

    def open_add_dialog(self):
        # Placeholder for add resource dialog
        print("Open Add Resource dialog")

    def open_add_dialog(self):

        window = ctk.CTkToplevel(self)
        window.title("Add Resource")
        window.geometry("400x350")

        campuses = self.service.get_campuses()

        campus_names = [c[1] for c in campuses]

        campus_menu = ctk.CTkOptionMenu(
            window,
            values=campus_names
        )

        campus_menu.pack(pady=15)

        name_entry = ctk.CTkEntry(
            window,
            placeholder_text="Resource Name"
        )

        name_entry.pack(pady=15)

        type_entry = ctk.CTkEntry(
            window,
            placeholder_text="Resource Type"
        )

        type_entry.pack(pady=15)

        def save():

            selected = campus_menu.get()

            campus_id = None

            for c in campuses:
                if c[1] == selected:
                    campus_id = c[0]

            self.service.add_resource(
                campus_id,
                name_entry.get(),
                type_entry.get()
            )

            window.destroy()

            self.load_resources()

        ctk.CTkButton(
            window,
            text="Save Resource",
            command=save
        ).pack(pady=20)

    def open_edit_dialog(self, resource_id):

        resource = self.service.get_resource(resource_id)

        campuses = self.service.get_campuses()

        window = ctk.CTkToplevel(self)
        window.title("Edit Resource")
        window.geometry("420x420")

        campus_names = [c[1] for c in campuses]

        campus_menu = ctk.CTkOptionMenu(
            window,
            values=campus_names
        )
        campus_menu.pack(pady=15)

        # Select current campus
        for c in campuses:
            if c[0] == resource[1]:
                campus_menu.set(c[1])
                break

        name_entry = ctk.CTkEntry(window, width=300)
        name_entry.insert(0, resource[2])
        name_entry.pack(pady=10)

        type_entry = ctk.CTkEntry(window, width=300)
        type_entry.insert(0, resource[3])
        type_entry.pack(pady=10)

        status_menu = ctk.CTkOptionMenu(
            window,
            values=[
                "Available",
                "Booked",
                "Maintenance",
                "Inactive"
            ]
        )

        status_menu.set(resource[4])
        status_menu.pack(pady=15)

        def save():

            campus_id = None

            for c in campuses:
                if c[1] == campus_menu.get():
                    campus_id = c[0]
                    break

            self.service.update_resource(
                resource_id,
                campus_id,
                name_entry.get(),
                type_entry.get(),
                status_menu.get()
            )

            window.destroy()

            self.load_resources()

            CTkMessagebox(
                title="Success",
                message="Resource updated successfully.",
                icon="check"
            )

        ctk.CTkButton(
            window,
            text="Save Changes",
            command=save
        ).pack(pady=25)
