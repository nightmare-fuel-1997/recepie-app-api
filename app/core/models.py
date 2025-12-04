"""
Database models for the application.
"""
# models: Django's ORM module for defining database tables as Python classes
from django.db import models
# AbstractBaseUser: Base class for custom user model (provides password
#   hashing, authentication, but NO fields - you define your own)
# BaseUserManager: Base class for custom user manager (handles user creation)
# PermissionsMixin: Adds permission-related fields (is_superuser, groups,
#   user_permissions) and methods (has_perm, has_module_perms)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    A manager is the interface for database query operations.
    User.objects.create_user() calls this manager's create_user method.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.

        Args:
            email: User's email address (required, used as username)
            password: User's password (optional, will be hashed)
            **extra_fields: Any additional fields (name, is_active, etc.)

        Returns:
            The created User instance

        Raises:
            ValueError: If email is empty
        """
        # Validate that email is provided (empty string is falsy in Python)
        if not email:
            raise ValueError('The Email field must be set')

        # normalize_email() lowercases the domain part of the email
        # e.g., "User@EXAMPLE.COM" -> "User@example.com"
        # This is inherited from BaseUserManager
        email = self.normalize_email(email)

        # self.model refers to the User class this manager is attached to
        # This creates a User instance but doesn't save it yet
        user = self.model(email=email, **extra_fields)

        # set_password() hashes the password using Django's password hasher
        # (PBKDF2 by default). NEVER store plain-text passwords!
        # If password is None, sets an unusable password (can't log in)
        # This method is inherited from AbstractBaseUser
        user.set_password(password)

        # Save the user to the database
        # using=self._db ensures it uses the correct database
        # (important for multi-database setups)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        Superusers have all permissions and can access the admin site.

        This method is called by: python manage.py createsuperuser
        """
        # setdefault() sets the value only if the key doesn't exist
        # This ensures superusers have staff and superuser status
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Double-check that the flags are True
        # (in case someone explicitly passed is_staff=False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Reuse create_user() to avoid code duplication
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the unique identifier
    instead of Django's default username.

    Inherits from:
    - AbstractBaseUser: Provides password field, authentication methods
    - PermissionsMixin: Provides is_superuser, groups, permissions
    """

    # EmailField: Validates email format, stored as VARCHAR(255)
    # unique=True: No two users can have the same email (also creates DB index)
    email = models.EmailField(max_length=255, unique=True)

    # CharField: Simple text field, stored as VARCHAR(255)
    name = models.CharField(max_length=255)

    # BooleanField: True/False field
    # is_active: Can this user log in? Set False to "soft delete" a user
    is_active = models.BooleanField(default=True)

    # is_staff: Can this user access the Django admin site?
    is_staff = models.BooleanField(default=False)

    # Attach our custom manager to this model
    # This enables: User.objects.create_user(), User.objects.create_superuser()
    objects = UserManager()

    # Tell Django to use 'email' field for authentication instead of 'username'
    # This is used by: authenticate(), login(), admin, etc.
    USERNAME_FIELD = 'email'

    def __str__(self):
        """
        String representation of the User.
        Used in admin, shell, and anywhere Python needs to display the user.
        e.g., print(user) -> "user@example.com"
        """
        return self.email
