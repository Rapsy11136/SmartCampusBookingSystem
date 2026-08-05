from services.auth_service import AuthService

auth = AuthService()

success, message = auth.register(
    "John Smith",
    "john@gmail.com",
    "123456",
    "Lecturer"
)

print(success)
print(message)

success, user = auth.login(
    "john@gmail.com",
    "123456"
)

print(success)
print(user)