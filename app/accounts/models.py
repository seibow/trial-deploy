from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)          # ← ハッシュ化
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=128)  # AbstractBaseUserで必要
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = "email"           # ← メールでログイン
    REQUIRED_FIELDS = ["username"]     # createsuperuser用。使わなければあっても害なし

    def __str__(self):
        return self.username