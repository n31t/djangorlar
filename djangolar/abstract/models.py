from email.policy import default
from django.db import models
from typing import Any
from django.utils import timezone


class CreatedAtMixin(models.Model):
    """
    Mixin for created at field in models
    """
    created_at : models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
class UpdatedAtMixin(models.Model):
    """
    Mixin for updated at field in models
    """
    updated_at : models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class IsActiveMixin(models.Model):
    """
    Mixin for deleted at field in models
    """
    is_active : models.DateTimeField(default=True)
    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """
    QuerySet for soft delete field in models
    """
    def delete(self) -> None:
        """
        Soft delete the objects in the QuerySet
        """
        return self.update(deleted_at=timezone.now())

    def hard_delete(self) -> None:
        """
        Hard delete the objects in the QuerySet
        """
        return super().delete()

class SoftDeleteManager(models.Manager):
    """
    Manager for soft delete field in models
    """
    def get_queryset(self) -> SoftDeleteQuerySet:
        """
        Get the QuerySet for the model
        """
        return SoftDeleteQuerySet(self.model, using=self._db)

class SoftDeleteMixin(models.Model):
    """
    Mixin for soft delete field in models
    """
    deleted_at : models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager()
    class Meta:
        abstract = True
    
    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """
        Soft delete the object
        """
        self.deleted_at = timezone.now()
        update_fields = ['deleted_at']

        additional_fields = self._prepare_soft_delete()
        if additional_fields:
            update_fields.extend(additional_fields)
        self.save(update_fields=update_fields)

    def _prepare_soft_delete(self) -> list[str]:
        """
        Prepare the additional fields for the soft delete
        """
        return []
    
    def hard_delete(self, using: str = None, keep_parents: bool = False) -> None:
        """
        Hard delete the object
        """
        super().delete(using=using, keep_parents=keep_parents)

class VersioningMixin(models.Model):
    """
    Mixin for versioning field in models
    """
    version : models.PositiveIntegerField(default=0)
    class Meta:
        abstract = True
    
    def bump_version(self) -> None:
        """
        Bump the version of the object
        """
        self.version = (self.version or 0) + 1

class BaseEntity(CreatedAtMixin, UpdatedAtMixin, IsActiveMixin, SoftDeleteMixin, VersioningMixin, models.Model):
    """
    Base entity model for all models
    """
    class Meta:
        abstract = True
    
    def _prepare_soft_delete(self) -> list[str]:
        """
        Prepare the additional fields for the soft delete
        """
        self.is_active = False
        return ['is_active']

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self,  *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
