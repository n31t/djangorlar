from django.db import models
from typing import Any
from django.utils import timezone
class CreatedAtMixin(models.Model):
    """
    Adds a created_at field to the model

    Fields:
        created_at: TimeStamp automatically set on insert
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    """
    Adds updated_at field to the model

    Fields:
        updated_at: TimeStamp automatically set on each save()
    """
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IsActiveMixin(models.Model):
    """
    Adds is_active field to the model for enabling/disabling records

    Fields:
        is_active: Boolean flag for active status
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """
    QuerySet for models with soft delete support.
    """
    def delete(self):
        """Soft delete all objects in the queryset"""
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all objects in the queryset"""
        return super().delete()


class SoftDeleteManager(models.Manager):
    """Manager that provides SoftDeleteQuerySet with utility methods"""
    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteMixin(models.Model):
    """
    Enables soft deletion via 'deleted_at' timestamp.

    Provides:
        - deleted_at field
        - Soft delete on instance.delete()
        - Template method for extensions
    """
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using: str | None = None, keep_parents: bool = False) -> None:
        """
        Soft delete by setting deleted_at timestamp.
        Calls _prepare_soft_delete() hook for extensions.
        """
        self.deleted_at = timezone.now()
        update_fields = ['deleted_at']

        additional_fields = self._prepare_soft_delete()
        if additional_fields:
            update_fields.extend(additional_fields)

        self.save(update_fields=update_fields)

    def _prepare_soft_delete(self) -> list[str]:
        """
        Hook for subclasses to perform additional actions during soft delete.

        Returns:
            List of additional field names to include in update_fields
        """
        return []

    def hard_delete(self, using: str | None = None, keep_parents: bool = False) -> None:
        """Permanently delete the record from database"""
        super().delete(using=using, keep_parents=keep_parents)


class VersionedMixin(models.Model):
    """
    Adds optimistic locking support by 'version' field

    Contract:
        Increment 'version' from service layer when applying state-changing updated
    """
    version = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True

    def bump_version(self):
        self.version = (self.version or 0) + 1


class BaseEntity(CreatedAtMixin, UpdatedAtMixin, IsActiveMixin, SoftDeleteMixin, VersionedMixin, models.Model):
    """
    Abstract base entity model

    Includes:
        - created_at, updated_at (timestamp tracking)
        - is_active (enable/disable flag)
        - deleted_at (soft delete)
        - version (optimistic lock)

    Behavior:
        - When soft deleted, is_active is automatically set to False
    """

    class Meta:
        abstract = True

    def _prepare_soft_delete(self) -> list[str]:
        """
        Coordinate soft delete with is_active flag.
        When soft deleting, also mark the record as inactive.
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
