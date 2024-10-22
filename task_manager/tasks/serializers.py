from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "task_type",
            "completed_at",
            "status",
            "created_by",
            "assigned_to",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "created_by",
        ]

    def create(self, validated_data):
        assigned_users = validated_data.pop(
            "assigned_to", None
        )
        task = Task.objects.create(**validated_data)

        if assigned_users:
            task.assigned_to.set(assigned_users)
        return task

    def update(self, instance, validated_data):
        assigned_users = validated_data.pop(
            "assigned_to", None
        )

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.task_type = validated_data.get("task_type", instance.task_type)
        instance.completed_at = validated_data.get(
            "completed_at", instance.completed_at
        )
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        if assigned_users is not None:
            instance.assigned_to.set(
                assigned_users
            )

        return instance


class AssignUserToTaskSerializer(serializers.Serializer):
    task = serializers.IntegerField(required=True)
    assign_to = serializers.IntegerField(required=True)
