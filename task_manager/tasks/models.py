from enum import Enum

from django.db import models
from django.contrib.auth.models import User


class TaskType(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace("_", " ").title()) for key in cls]


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace("_", " ").title()) for key in cls]


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=100, choices=TaskType.choices())
    status = models.CharField(
        max_length=50,
        choices=TaskStatus.choices(),
        default="pending",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )
    assigned_to = models.ManyToManyField(User, related_name="assigned_tasks")

    def __str__(self):
        return self.name
