from django.urls import path

from . import views

app_name = "versions"

urlpatterns = [
    path("", views.VersionsView.as_view(), name="version"),
]
