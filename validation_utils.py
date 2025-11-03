"""
Validation Utilities Module

This module provides comprehensive validation functions for various data types,
formats, and business logic validations.
"""

import re
from typing import Any, List, Dict, Optional, Callable, Union
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __bool__(self):
        """Allow using ValidationResult in boolean context."""
        return self.is_valid

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)


class StringValidator:
    """Validator for string values."""

    @staticmethod
    def is_not_empty(value: str, field_name: str = "Field") -> ValidationResult:
        """Check if string is not empty."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if not value or not value.strip():
            result.add_error(f"{field_name} cannot be empty")

        return result

    @staticmethod
    def min_length(value: str, min_len: int, field_name: str = "Field") -> ValidationResult:
        """Check minimum string length."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if len(value) < min_len:
            result.add_error(f"{field_name} must be at least {min_len} characters long")

        return result

    @staticmethod
    def max_length(value: str, max_len: int, field_name: str = "Field") -> ValidationResult:
        """Check maximum string length."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if len(value) > max_len:
            result.add_error(f"{field_name} must not exceed {max_len} characters")

        return result

    @staticmethod
    def matches_pattern(value: str, pattern: str, field_name: str = "Field",
                       error_message: Optional[str] = None) -> ValidationResult:
        """Check if string matches a regex pattern."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if not re.match(pattern, value):
            msg = error_message or f"{field_name} format is invalid"
            result.add_error(msg)

        return result

    @staticmethod
    def is_email(value: str) -> ValidationResult:
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return StringValidator.matches_pattern(
            value, email_pattern, "Email", "Invalid email format"
        )

    @staticmethod
    def is_url(value: str) -> ValidationResult:
        """Validate URL format."""
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return StringValidator.matches_pattern(
            value, url_pattern, "URL", "Invalid URL format"
        )

    @staticmethod
    def is_phone_number(value: str) -> ValidationResult:
        """Validate phone number format."""
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)]', '', value)
        phone_pattern = r'^\+?[\d]{10,15}$'
        return StringValidator.matches_pattern(
            cleaned, phone_pattern, "Phone number", "Invalid phone number format"
        )


class NumberValidator:
    """Validator for numeric values."""

    @staticmethod
    def is_positive(value: Union[int, float, Decimal], field_name: str = "Value") -> ValidationResult:
        """Check if number is positive."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if value <= 0:
            result.add_error(f"{field_name} must be positive")

        return result

    @staticmethod
    def is_non_negative(value: Union[int, float, Decimal], field_name: str = "Value") -> ValidationResult:
        """Check if number is non-negative."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if value < 0:
            result.add_error(f"{field_name} must be non-negative")

        return result

    @staticmethod
    def in_range(value: Union[int, float, Decimal], min_val: Union[int, float, Decimal],
                 max_val: Union[int, float, Decimal], field_name: str = "Value") -> ValidationResult:
        """Check if number is within a range."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if value < min_val or value > max_val:
            result.add_error(f"{field_name} must be between {min_val} and {max_val}")

        return result

    @staticmethod
    def is_integer(value: Any, field_name: str = "Value") -> ValidationResult:
        """Check if value can be converted to integer."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        try:
            int(value)
        except (ValueError, TypeError):
            result.add_error(f"{field_name} must be a valid integer")

        return result

    @staticmethod
    def is_decimal(value: Any, field_name: str = "Value", max_digits: Optional[int] = None,
                   decimal_places: Optional[int] = None) -> ValidationResult:
        """Check if value is a valid decimal."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        try:
            decimal_value = Decimal(str(value))

            if max_digits is not None or decimal_places is not None:
                parts = str(decimal_value).split('.')
                integer_part = parts[0].lstrip('-')
                fractional_part = parts[1] if len(parts) > 1 else ''

                if max_digits is not None:
                    total_digits = len(integer_part) + len(fractional_part)
                    if total_digits > max_digits:
                        result.add_error(f"{field_name} has too many digits (max: {max_digits})")

                if decimal_places is not None and len(fractional_part) > decimal_places:
                    result.add_error(f"{field_name} has too many decimal places (max: {decimal_places})")

        except (ValueError, InvalidOperation):
            result.add_error(f"{field_name} must be a valid decimal number")

        return result


class DateValidator:
    """Validator for date and datetime values."""

    @staticmethod
    def is_past_date(value: Union[date, datetime], field_name: str = "Date") -> ValidationResult:
        """Check if date is in the past."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        current_date = datetime.now().date() if isinstance(value, date) else datetime.now()

        if value >= current_date:
            result.add_error(f"{field_name} must be in the past")

        return result

    @staticmethod
    def is_future_date(value: Union[date, datetime], field_name: str = "Date") -> ValidationResult:
        """Check if date is in the future."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        current_date = datetime.now().date() if isinstance(value, date) else datetime.now()

        if value <= current_date:
            result.add_error(f"{field_name} must be in the future")

        return result

    @staticmethod
    def is_within_range(value: Union[date, datetime], start: Union[date, datetime],
                       end: Union[date, datetime], field_name: str = "Date") -> ValidationResult:
        """Check if date is within a range."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if value < start or value > end:
            result.add_error(f"{field_name} must be between {start} and {end}")

        return result

    @staticmethod
    def parse_date_string(value: str, format_string: str = "%Y-%m-%d",
                         field_name: str = "Date") -> ValidationResult:
        """Parse and validate a date string."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        try:
            datetime.strptime(value, format_string)
        except ValueError:
            result.add_error(f"{field_name} must be in format {format_string}")

        return result


class CollectionValidator:
    """Validator for lists, dictionaries, and other collections."""

    @staticmethod
    def is_not_empty(collection: Union[List, Dict, set, tuple],
                     field_name: str = "Collection") -> ValidationResult:
        """Check if collection is not empty."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if not collection:
            result.add_error(f"{field_name} cannot be empty")

        return result

    @staticmethod
    def min_items(collection: Union[List, Dict, set, tuple], min_count: int,
                  field_name: str = "Collection") -> ValidationResult:
        """Check minimum number of items."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if len(collection) < min_count:
            result.add_error(f"{field_name} must contain at least {min_count} items")

        return result

    @staticmethod
    def max_items(collection: Union[List, Dict, set, tuple], max_count: int,
                  field_name: str = "Collection") -> ValidationResult:
        """Check maximum number of items."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if len(collection) > max_count:
            result.add_error(f"{field_name} must not exceed {max_count} items")

        return result

    @staticmethod
    def all_unique(collection: List, field_name: str = "Collection") -> ValidationResult:
        """Check if all items in collection are unique."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        if len(collection) != len(set(collection)):
            result.add_error(f"{field_name} must contain only unique items")

        return result


class CompositeValidator:
    """Combine multiple validators."""

    def __init__(self):
        """Initialize the composite validator."""
        self.validators: List[Callable] = []

    def add_validator(self, validator: Callable) -> 'CompositeValidator':
        """Add a validator function."""
        self.validators.append(validator)
        return self

    def validate(self, value: Any) -> ValidationResult:
        """Run all validators and combine results."""
        combined_result = ValidationResult(is_valid=True, errors=[], warnings=[])

        for validator in self.validators:
            result = validator(value)
            if not result.is_valid:
                combined_result.is_valid = False
            combined_result.errors.extend(result.errors)
            combined_result.warnings.extend(result.warnings)

        return combined_result


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """Validate that all required fields are present in a dictionary."""
    result = ValidationResult(is_valid=True, errors=[], warnings=[])

    for field in required_fields:
        if field not in data or data[field] is None:
            result.add_error(f"Required field '{field}' is missing")

    return result
