# Python modules
from typing import Optional, Sequence

from django.contrib.admin import ModelAdmin, register, TabularInline
from django.core.handlers.wsgi import WSGIRequest

from tasks.models import Task, UserTask, Project


@register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
        "created_at"
    )
    list_display_links = (
        "id",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "name",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    filter_horizontal = (
        "users",
    )
    save_on_top = True
    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "name",
                    "author",
                    "users",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            }
        )
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: Optional[Project] = None) -> bool:
        return True

    def has_change_permission(self, request: WSGIRequest, obj: Optional[Project] = None) -> bool:
        return True


class UserTaskInline(TabularInline):
    model = UserTask
    extra = 1
    fields = ('user',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')


@register(Task)
class TaskAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
        "project",
        "parent",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "name",
        "description",
        "project__name",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
        "project",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (UserTaskInline,)
    save_on_top = True
    fieldsets = (
        (
            "Task Information",
            {
                "fields": (
                    "name",
                    "description",
                    "status",
                    "project",
                    "parent",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            }
        )
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: Optional[Task] = None) -> bool:
        return True

    def has_change_permission(self, request: WSGIRequest, obj: Optional[Task] = None) -> bool:
        return True


@register(UserTask)
class UserTaskAdmin(ModelAdmin):
    list_display = (
        "id",
        "task",
        "user",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "task__name",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "task__project",
        "task__status",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    save_on_top = True
    fieldsets = (
        (
            "Assignment Information",
            {
                "fields": (
                    "task",
                    "user",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            }
        )
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: Optional[UserTask] = None) -> bool:
        return True

    def has_change_permission(self, request: WSGIRequest, obj: Optional[UserTask] = None) -> bool:
        return True