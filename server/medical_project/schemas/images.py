from rest_framework import serializers

from core.views import BaseSchemaMixin
from medical_project.models import ImageFile

from .annotations import AnnotationCreateSchema


class UploadImageAndAnnotationSchema(BaseSchemaMixin, serializers.ModelSerializer):
    annotation = AnnotationCreateSchema(allow_null=True, required=False)

    class Meta:
        model = ImageFile
        fields = ["image", "annotation"]

    def create(self, validated_data: dict) -> ImageFile:
        annotation_data = validated_data.pop("annotation", None)
        image_file = ImageFile.objects.create(**validated_data)

        if annotation_data:
            annotation_data["parent"] = (
                annotation_data["parent"].id if annotation_data.get("parent") else None
            )
            annotation_serializer = AnnotationCreateSchema(data=annotation_data)
            if annotation_serializer.is_valid(raise_exception=True):
                annotation_serializer.save(image_file=image_file)
        return image_file
