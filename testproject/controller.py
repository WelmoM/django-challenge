from django.contrib.auth.models import User

class UserController:
    def user_account_creation(self, username: str, email: str, password: str) -> bool:
        if not username or not email or not password:
            return False
        try:
            if User.objects.filter(username=username).exists():
                return False
            User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            print(e)
            return False
        return True