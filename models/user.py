import hashlib


class User:
    def __init__(self, fullname, email, password, role):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password, hashed_password):
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password