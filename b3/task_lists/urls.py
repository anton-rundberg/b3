from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "task_list"

router = routers.DefaultRouter()
router.register("list", views.ListViewSet, basename="list")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "list/<uuid:pk>/task/<uuid:task_id>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "list/<uuid:pk>/task/",
        views.TaskView.as_view(),
        name="task-list",
    ),
]
