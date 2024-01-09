from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        task = Task.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            task.tags.add(tag)

        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        instance = super().update(instance, validated_data)

        # Add new tags and keep existing ones
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            if created:
                instance.tags.add(tag)

        return instance

    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {"tags": {"required": False}}
        read_only_fields = ("timestamp",)

    def get_serializer(self, *args, **kwargs):
        # Set partial=True for partial updates
        kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)
