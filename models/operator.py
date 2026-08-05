from models.user import User


class SystemOperator(User):
    def __init__(self, fullname, email, password):
        super().__init__(fullname, email, password, "System Operator")