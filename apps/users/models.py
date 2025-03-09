from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None, role='student', **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            firstName=firstName, 
            lastName=lastName, 
            role=role, 
            **extra_fields
        )
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password=None, **extra_fields):
        return self.create_user(email, firstName, lastName, password, role='admin', **extra_fields)

# Custom User Model
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'role']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    def clean(self):
        if not self.firstName:
            raise ValidationError('First name is required')
        if not self.lastName:
            raise ValidationError('Last name is required')
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError('Invalid role') 
