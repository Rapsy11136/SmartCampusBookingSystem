from models.user import User


class CampusAdmin(User):
    def __init__(self, fullname, email, password):
        super().__init__(fullname, email, password, "Campus Administrator")