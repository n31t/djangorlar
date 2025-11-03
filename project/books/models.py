from typing import Any
from django.db import models

from django.db.models import (
    PROTECT,
)
from abstract.models import AbstractBaseModel

from django.contrib.auth.models import User

class Book(AbstractBaseModel):
    """
    Book database model
    """
    NAME_MAX_LENGTH=1000

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description= models.TextField()
    author = models.ForeignKey(
        to= User,
        blank=False,
        on_delete=PROTECT
    )

    def __repr__(self):
        """ Returns official representation of the book """
        return f"Book(name={self.name}, author={self.author})"
    
    def __str__(self):
        """ Returns string representation of the book """
        return self.name

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """Override delete method to perform soft delete."""
        super().delete(*args, **kwargs)

    



