from db_manager import Database
from models.user import User


class AuthService:

    def __init__(self):
        self.db = Database()

    # ==========================================================
    # GET CAMPUSES
    # ==========================================================

    def get_campuses(self):

        return self.db.fetchall("""
            SELECT
                id,
                name
            FROM campuses
            ORDER BY name
        """)

    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(
            self,
            fullname,
            email,
            password,
            role,
            campus_id=None
    ):

        fullname = fullname.strip()
        email = email.strip().lower()
        role = role.strip()

        # =========================
        # VALIDATION
        # =========================

        if not fullname:
            return False, "Full name is required."

        if not email:
            return False, "Email is required."

        if not password:
            return False, "Password is required."

        if not role:
            return False, "Role is required."

        # =========================
        # CAMPUS VALIDATION
        # =========================

        if role != "System Operator":

            if campus_id is None:
                return False, "Campus selection is required."

            campus = self.db.fetchone(
                """
                SELECT id
                FROM campuses
                WHERE id=?
                """,
                (campus_id,)
            )

            if not campus:
                return False, "Selected campus does not exist."

        # =========================
        # CHECK EMAIL
        # =========================

        existing = self.db.fetchone(
            """
            SELECT id
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        if existing:

            return False, "Email already exists."

        # =========================
        # HASH PASSWORD
        # =========================

        hashed = User.hash_password(password)

        # =========================
        # INSERT USER
        # =========================

        self.db.execute(
            """
            INSERT INTO users(
                fullname,
                email,
                password,
                role,
                campus_id
            )
            VALUES(?,?,?,?,?)
            """,
            (
                fullname,
                email,
                hashed,
                role,
                campus_id
            )
        )

        return True, "Registration successful."

    # ==========================================================
    # LOGIN
    # ==========================================================

    def login(self, email, password):

        email = email.strip().lower()

        if not email or not password:

            return False, "Email and password are required."

        user = self.db.fetchone(
            """
            SELECT
                id,
                fullname,
                email,
                password,
                role,
                campus_id
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        if not user:

            return False, "Invalid email or password."

        # Verify hashed password
        if not User.verify_password(
                password,
                user[3]
        ):

            return False, "Invalid email or password."

        return True, user