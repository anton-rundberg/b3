from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from . import models, serializers


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.List.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {
            "list_id": self.kwargs["pk"],
            "task_id": self.kwargs["task_id"],
            **super().get_serializer_context(),
        }

    def get_object(self):
        return get_object_or_404(
            models.Task.objects,
            list__user=self.request.user,
            pk=self.kwargs["task_id"],
        )


class TaskView(generics.ListCreateAPIView):
    serializer_class = serializers.TaskCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {
            "list_id": self.kwargs["pk"],
            **super().get_serializer_context(),
        }

    def get_queryset(self):
        return models.Task.objects.filter(
            list=self.kwargs["pk"],
            list__user=self.request.user,
        ).order_by("-created_at")
