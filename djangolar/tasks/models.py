from django.contrib.auth import get_user_model
from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    PROTECT,
    CASCADE,
)
from abstract.models import AbstractBaseModel


User = get_user_model()

class Project(AbstractBaseModel):
    NAME_MAX_LEN = 100

    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    author = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name="owned_projects",
    )
    users = ManyToManyField(
        to=User,
        blank=True,
        related_name="joined_projects",
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id}, name={self.name})"

    def __str__(self) -> str:
        return self.name


class Task(AbstractBaseModel):
    NAME_MAX_LEN = 200
    STATUS_TODO = 1
    STATUS_TODO_LABEL = "To Do"
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PROGRESS_LABEL = "In Progress"
    STATUS_DONE = 3
    STATUS_DONE_LABEL = "Done"
    STATUS_CHOICES = {
        STATUS_TODO: STATUS_TODO_LABEL,
        STATUS_IN_PROGRESS: STATUS_IN_PROGRESS_LABEL,
        STATUS_DONE: STATUS_DONE_LABEL,
    }

    name = CharField(
        max_length=NAME_MAX_LEN,
        db_index=True,
    )
    description = TextField(
        blank=True,
        default="",
    )
    status = IntegerField(
        default=STATUS_TODO,
        choices=STATUS_CHOICES,
    )
    parent = ForeignKey(
        to="self",
        on_delete=CASCADE,
        null=True,
        blank=True,
    )
    project = ForeignKey(
        to=Project,
        on_delete=CASCADE,
    )
    assignees = ManyToManyField(
        to=User,
        through="UserTask",
        through_fields=("task", "user"),
        blank=True,
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, name={self.name}, status={self.status})"

    def __str__(self) -> str:
        return self.name


class UserTask(AbstractBaseModel):
    task = ForeignKey(
        to=Task,
        on_delete=CASCADE,
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["task", "user"],
                name="unique_task_user",
            ),
        ]

    def __repr__(self) -> str:
        return f"UserTask(id={self.id}, task={self.task.name}, user={self.user.username})"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.task.name}"