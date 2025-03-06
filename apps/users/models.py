from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        return self.create_user(email, first_name, last_name, password, **extra_fields)
    

# Custom User Model
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    objects = UserManager()

    class Meta:
        db_table = 'user'  # Custom table name

    def __str__(self):
        return self.email

    def clean(self):
        if not self.firstName:
            raise ValidationError('First name is required')
        if not self.lastName:
            raise ValidationError('Last name is required')
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError('Invalid role')