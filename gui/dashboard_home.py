import customtkinter as ctk


class DashboardHome(ctk.CTkFrame):

    def __init__(self, master, user, total=0, available=0, booked=0):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text=f"Welcome, {user[1]}",
            font=("Arial", 28, "bold")
        ).pack(anchor="w", padx=30, pady=(30, 10))

        ctk.CTkLabel(
            self,
            text=f"Role: {user[4]}",
            font=("Arial", 18)
        ).pack(anchor="w", padx=30)

        cards = ctk.CTkFrame(self)
        cards.pack(fill="x", padx=30, pady=40)

        self.create_card(cards, "Resources", total).pack(side="left", padx=15)
        self.create_card(cards, "Available", available).pack(side="left", padx=15)
        self.create_card(cards, "Booked", booked).pack(side="left", padx=15)

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(parent, width=180, height=120)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18)
        ).pack(pady=15)

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 30, "bold")
        ).pack()

        return card