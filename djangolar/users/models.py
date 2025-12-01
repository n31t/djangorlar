# Python modules
from typing import Any

# Django modules
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateField,
    DecimalField
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Project modules
from abstract.models import AbstractBaseModel



class CustomUserManager(BaseUserManager):
    """Custom User Manager to make database requests."""

    def __obtain_user_instance(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Get user instance."""
        if not email:
            raise ValidationError(
                message="Email field is required", code="email_empty"
            )
        if not full_name:
            raise ValidationError(
                message="Full name name is required.", code="full_name_empty"
            )

        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
            **kwargs,
        )
        return new_user

    def create_user(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create Custom user. TODO where is this used?"""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create super user. Used by manage.py createsuperuser."""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Custom user model extending AbstractBaseModel.
    """
    EMAIL_MAX_LENGTH = 150
    FULL_NAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 254

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Email address",
        help_text="User's email address",
    )
    username = CharField(
        max_length=FULL_NAME_MAX_LENGTH,
        verbose_name="Username",
    )
    full_name = CharField(
        max_length=FULL_NAME_MAX_LENGTH,
        verbose_name="Full name",
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        validators=[validate_password],
        verbose_name="Password",
        help_text="User's hash representation of the password",
    )

    #additional info
    phone = CharField(
        max_length = 10,
        verbose_name = "Phone",
        blank = True,
        null = True,
    )
    city = CharField(
        max_length = 255,
        blank = True,
        null = True,
    )
    country = CharField(
        max_length = 255,
        blank = True,
        null = True,
    )
    department = CharField(
        choices = (("it", "IT"), ("hr", "HR"), ("sales", "SALES"), ("finance", "Finance")),
        max_length = 255,
    )
    role = CharField(
        choices = (("admin", "Admin"), ("manager", "Manager"), ("employee", "Employee")),
        max_length = 255,
    )
    birth_date = DateField(
        verbose_name="Birth date",
    )
    salary = DecimalField(
        verbose_name="Salary",
        null = True,
        blank = True,
        max_digits=10, 
        decimal_places=3
    )

    is_staff = BooleanField(
        default=False,
        verbose_name="Staff status",
        help_text="True if the user is an admin and has an access to the admin panel",
    )
    is_active = BooleanField(
        default=True,
        verbose_name="Active status",
        help_text="True if the user is active and has an access to request data",
    )

    REQUIRED_FIELDS = ["full_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        """Meta options for CustomUser model."""

        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-created_at"]

    def clean(self) -> None:
        """Validate the model instance before saving."""
        return super().clean()