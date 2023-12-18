from rest_framework import serializers

from core.views import BaseSchemaMixin
from medical_project.models import Annotation, Tags


class AnnotationCreateSchema(BaseSchemaMixin, serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.IntegerField(), required=False)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Annotation.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Annotation
        fields = "__all__"

    def create(self, validated_data: dict) -> Annotation:
        tags_data = validated_data.pop("tags", [])

        annotation = Annotation.objects.create(**validated_data)

        if tags_data:
            for tag_id in tags_data:
                tag_instance, _ = Tags.objects.get_or_create(tag=tag_id)
                annotation.tags.add(tag_instance)

        return annotation


class AnnotationUpdateSchema(BaseSchemaMixin, serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = [
            "class_id",
            "start_x",
            "start_y",
            "end_x",
            "end_y",
            "confirmed",
            "tags",
            "surface",
            "parent",
            "type",
            "confidence_percent",
            "image_file",
        ]
