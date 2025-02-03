from rest_framework import serializers

from . import models


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.List
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)

    def save(self, **kwargs):
        return super().save(
            user=self.context["request"].user,
            **kwargs,
        )


class TaskSerializer(serializers.ModelSerializer):

    list_id = serializers.UUIDField()

    class Meta:
        model = models.Task
        fields = (
            "id",
            "list_id",
            "name",
            "description",
        )
        read_only_fields = ("id",)

    def save(self, **kwargs):
        return super().save(
            list_id=self.context["list_id"],
            **kwargs,
        )

    def validate_list_id(self, list_id):
        is_list_owner = models.List.objects.filter(
            pk=list_id,
            user=self.context["request"].user,
        ).exists()
        if not is_list_owner:
            raise serializers.ValidationError(
                {"id": "You are not the owner of this list!"}
            )

    def validate(self, attrs):
        is_task_owner = models.Task.objects.filter(
            pk=self.context["task_id"],
            list__user=self.context["request"].user,
        ).exists()
        if not is_task_owner:
            raise serializers.ValidationError(
                {"task_id": "You are not the owner of this task!"}
            )

        return attrs


class TaskCreateSerializer(serializers.ModelSerializer):
    list_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Task
        fields = (
            "id",
            "list_id",
            "name",
            "description",
        )
        read_only_fields = ("id",)

    def save(self, **kwargs):
        return super().save(
            list_id=self.context["list_id"],
            **kwargs,
        )
