import hashlib


class User:

    def __init__(
            self,
            fullname,
            email,
            password,
            role,
            campus_id=None
    ):

        self.fullname = fullname
        self.email = email
        self.password = password
        self.role = role
        self.campus_id = campus_id

    # ==========================================================
    # HASH PASSWORD
    # ==========================================================

    @staticmethod
    def hash_password(password):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    # ==========================================================
    # VERIFY PASSWORD
    # ==========================================================

    @staticmethod
    def verify_password(
            password,
            hashed_password
    ):

        return hashlib.sha256(
            password.encode()
        ).hexdigest() == hashed_password