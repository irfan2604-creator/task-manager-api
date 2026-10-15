from rest_framework import serializers
from .models import Task ,Category


class TaskSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(
        required=False,
        allow_null=True,
        validators=[],
    )

    def validate_attachment(self, value):
        if value is None:
            return value

        max_size = 5 * 1024 * 1024  # 5 MB
        allowed_extensions = {".pdf", ".txt", ".png", ".jpg", ".jpeg"}

        if value.size > max_size:
            raise serializers.ValidationError(
                "File size cannot exceed 5 MB."
            )

        import os

        extension = os.path.splitext(value.name)[1].lower()
        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Unsupported file type."
            )

        return value

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "owner")

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate(self, data):
        status = data.get("status")
        description = data.get("description")

        if status == "COMPLETED" and not description:
            raise serializers.ValidationError(
                "Completed tasks must have a description."
            )

        return data
    def validate_category(self, value):
        if value and value.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only assign tasks to your own categories.")
        return value
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "id", "name", "owner"
        read_only_fields = ("id", "owner") 