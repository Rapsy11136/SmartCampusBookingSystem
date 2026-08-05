from db_manager import Database


class UserService:

    def __init__(self):
        self.db = Database()

    def get_users(self):
        return self.db.fetchall("""
            SELECT
                id,
                fullname,
                email,
                role
            FROM users
            ORDER BY fullname
        """)

    def add_user(self, fullname, email, password, role):

        self.db.execute("""
            INSERT INTO users
            (fullname,email,password,role)
            VALUES(?,?,?,?)
        """,
        (
            fullname,
            email,
            password,
            role
        ))

    def update_user(
        self,
        user_id,
        fullname,
        email,
        role
    ):

        self.db.execute("""
            UPDATE users

            SET
                fullname=?,
                email=?,
                role=?

            WHERE id=?
        """,
        (
            fullname,
            email,
            role,
            user_id
        ))

    def delete_user(self, user_id):

        self.db.execute("""
            DELETE FROM users
            WHERE id=?
        """, (user_id,))

    def search_users(self, keyword):

        keyword = f"%{keyword}%"

        return self.db.fetchall("""
            SELECT
                id,
                fullname,
                email,
                role
            FROM users
            WHERE
                fullname LIKE ?
                OR email LIKE ?
                OR role LIKE ?
            ORDER BY fullname
        """,
        (
            keyword,
            keyword,
            keyword
        ))