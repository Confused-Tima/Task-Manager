from django.urls import path

from . import views


urlpatterns = [
    path(
        "get-static-task-data/", views.get_static_task_data, name="get_static_task_data"
    ),
    path("create-task/", views.create_task, name="create_task"),
    path("assign-task/", views.assign_task, name="assign_task"),
    path("remove-assignee/", views.remove_assignee, name="remove_assignee"),
    path("get-tasks/", views.get_tasks, name="get_tasks"),
]
