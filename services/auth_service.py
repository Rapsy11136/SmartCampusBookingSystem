from db_manager import Database
from models.user import User


class AuthService:

    def __init__(self):
        self.db = Database()

    def register(self, fullname, email, password, role):

        fullname = fullname.strip()
        email = email.strip().lower()

        if not fullname:
            return False, "Full name is required."

        if not email:
            return False, "Email is required."

        if not password:
            return False, "Password is required."

        existing = self.db.fetchone(
            "SELECT id FROM users WHERE email=?",
            (email,)
        )

        if existing:
            return False, "Email already exists."

        hashed = User.hash_password(password)

        self.db.execute(
            """
            INSERT INTO users(fullname,email,password,role)
            VALUES(?,?,?,?)
            """,
            (
                fullname,
                email,
                hashed,
                role
            )
        )

        return True, "Registration successful."

    def login(self, email, password):

        email = email.strip().lower()

        user = self.db.fetchone(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        if not user:
            return False, "Invalid email or password."

        if not User.verify_password(password, user[3]):
            return False, "Invalid email or password."

        return True, user