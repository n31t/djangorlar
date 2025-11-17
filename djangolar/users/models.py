from typing import Any

from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateField,
    DecimalField,
    DateTimeField,
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager for db
    """
    def __obtain_user_instance(self, email: str, full_name:str, password: str, **kwargs: dict[str, Any]) -> 'CustomUser':
        """Get user instance by email and password"""
        if not email:
            raise ValidationError(message="Email is required", code="email_required")
        if not full_name:
            raise ValidationError(message="Full name is required", code="full_name_required")
        if not password:
            raise ValidationError(message="Password is required", code="password_required")
        new_user: 'CustomUser' = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            password = password,
            **kwargs
        )
        return new_user
    
    def create_user(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        """Create and save a user with the given email and password."""
        new_user: 'CustomUser' = self.__obtain_user_instance(email, full_name, password, **kwargs)
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        """Create and save a superuser with the given email and password."""
        new_user: 'CustomUser' = self.__obtain_user_instance(email, full_name, password, **kwargs)
        new_user.set_password(password)
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for db
    """

    EMAIL_MAX_LEN = 150
    FULL_NAME_MAX_LEN = 150
    PASSWORD_MAX_LEN = 254
    PHONE_MAX_LEN = 20
    CITY_MAX_LEN = 100
    COUNTRY_MAX_LEN = 100
    DEPARTMENT_MAX_LEN = 100
    ROLE_MAX_LEN = 100

    email = EmailField(
        max_length=EMAIL_MAX_LEN,
        unique=True,
        db_index=True,
        verbose_name="email address",
        help_text="The email address of the user",
    )
    username = CharField(
        max_length=FULL_NAME_MAX_LEN,
        verbose_name="username",
    )
    full_name = CharField(
        max_length=FULL_NAME_MAX_LEN,
        verbose_name="full name",
    )
    password = CharField(
        max_length=PASSWORD_MAX_LEN,
        validators=[validate_password],
        verbose_name="password",
    )

    phone = CharField(
        max_length=PHONE_MAX_LEN,
        verbose_name="phone",
        help_text="The phone number of the user",
    )
    city = CharField(
        max_length=CITY_MAX_LEN,
        verbose_name="city",
        help_text="The city of the user",
    )

    country = CharField(
        max_length=COUNTRY_MAX_LEN,
        verbose_name="country",
        help_text="The country of the user",
    )

    department = CharField(
        max_length=DEPARTMENT_MAX_LEN,
        verbose_name="department",
        help_text="The department of the user",
    )

    role = CharField(
        choices=(('admin', 'Admin'), ('manager', 'Manager'), ('employee', 'Employee')),
        max_length=ROLE_MAX_LEN,
    )
    birth_date = DateField(
        verbose_name="birth date",
        help_text="The birth date of the user",
    )
    salary = DecimalField(
        max_digits=10,
        decimal_places=2,
        blank = True,
        null = True,
        verbose_name="salary",
        help_text="The salary of the user",
    )

    is_staff = BooleanField(
        default=False,
        verbose_name="staff status",
        help_text="Whether the user can log into this admin site.",
    )
    is_active = BooleanField(
        default=True,
        verbose_name="active",
        help_text="Whether the user can log into this admin site.",
    )
    date_joined = DateTimeField(
        default=timezone.now,
        verbose_name="date joined",
        help_text="The date and time the user joined the site.",
    )

    last_login = DateTimeField(
        blank=True,
        null=True,
        verbose_name="last login",
        help_text="The date and time the user last logged in.",
    )

    REQUIRED_FIELDS=['full_name']
    USERNAME_FIELD='email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['-date_joined']

    def clean(self) -> None:
        """Clean the user data"""
        return super().clean()