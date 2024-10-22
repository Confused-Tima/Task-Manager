from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotFound, NotAcceptable

from users.permissions import WriteOnlyIfAuthenticated
from .models import Task, TaskStatus, TaskType
from .serializers import TaskSerializer, AssignUserToTaskSerializer
from users.serializers import UserBasicSerializer


@api_view(["GET"])
def get_static_task_data(_: Request):
    """API to get static data related to tasks"""

    task_types = TaskType.choices()
    task_statuses = TaskStatus.choices()

    return Response(
        {"type": task_types, "status": task_statuses}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([WriteOnlyIfAuthenticated])
def create_task(request: Request):
    """API to create task"""

    serialized_data = TaskSerializer(data=request.data)

    # Auto raise exceptions if anything is invalid
    serialized_data.is_valid(raise_exception=True)

    task = serialized_data.save(created_by=request.user)

    return Response(
        {
            "task": TaskSerializer(task).data,
            "status": "created",
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([WriteOnlyIfAuthenticated])
def assign_task(request: Request):
    """API to assign task to a user"""

    serializer = AssignUserToTaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    task_id = serializer.validated_data["task"]
    user_id = serializer.validated_data["assign_to"]

    task = get_object_or_404(Task, id=task_id)
    if not task:
        raise NotFound("Task does not exist")  # If task doesn't exist

    user = get_object_or_404(User, id=user_id)
    if not user:
        raise NotFound("User does not exist")  # If user doesn't exist

    if task.assigned_to.filter(id=user.id).exists():
        raise NotAcceptable(
            "User is already assigned with this task"
        )  # If user already exists

    task.assigned_to.add(user)
    return Response(
        {
            "update_assignees": UserBasicSerializer(
                task.assigned_to.all(), many=True
            ).data,
            "status": "success",
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["DELETE"])
@permission_classes([WriteOnlyIfAuthenticated])
def remove_assignee(request: Request):
    """API to remove task from a user"""

    serializer = AssignUserToTaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    task_id = serializer.validated_data["task"]
    user_id = serializer.validated_data["assign_to"]

    task = get_object_or_404(Task, id=task_id)

    if not task.assigned_to.filter(id=user_id).exists():
        raise NotAcceptable(
            "User has not been assigned this task"
        )  # If user not even assigned the task

    task.assigned_to.remove(user_id)

    return Response(
        {
            "update_assignees": UserBasicSerializer(
                task.assigned_to.all(), many=True
            ).data,
            "status": "success",
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["GET"])
def get_tasks(request: Request):

    user_id = request.GET.get("user_id")
    username = request.GET.get("username")

    if user_id:
        user = get_object_or_404(User, id=user_id)
    if user_id:
        user = get_object_or_404(User, username=username)
    elif request.user.is_authenticated:
        user = request.user
    else:
        raise NotFound("User ID or Unique Username is Required to fetch the user")

    user_tasks = Task.objects.filter(assigned_to=user)

    return Response(
        {
            "status": "success",
            "data": user_tasks,
        }
    )
