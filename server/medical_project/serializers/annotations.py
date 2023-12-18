from django.db.models import Q
from rest_framework import serializers

from core.views import BaseSchemaMixin
from medical_project.models import Annotation, Tags


class AnnotationSerializer(BaseSchemaMixin, serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = "__all__"


class ExternalFormatSerializer(BaseSchemaMixin, serializers.ModelSerializer):
    kind = serializers.CharField(source="class_id")
    shape = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    surface = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Annotation
        fields = ("id", "kind", "shape", "number", "surface", "children")

    def get_shape(self, obj: Annotation) -> dict:
        return {"x": [obj.start_x, obj.end_x], "y": [obj.start_y, obj.end_y]}

    def get_number(self, obj: Annotation) -> dict:
        return obj.tags.values_list("tag", flat=True)

    def get_surface(self, obj: Annotation) -> str:
        return "".join(obj.surface)

    def get_children(self, obj: Annotation) -> list:
        children = Annotation.objects.filter(
            Q(image_file_id=obj.image_file_id) & Q(parent_id=obj.id)
        )
        if children:
            child_data = []
            for child in children:
                child_data.append(ExternalFormatSerializer(child).data)
            return child_data


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("tag",)


class InternalFormatSerializer(BaseSchemaMixin, serializers.ModelSerializer):
    shape = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    relations = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = Annotation
        fields = ("id", "class_id", "surface", "shape", "tags", "relations", "meta")

    def get_shape(self, obj: Annotation) -> dict:
        return {
            "end_x": obj.end_x,
            "end_y": obj.end_y,
            "start_x": obj.start_x,
            "start_y": obj.start_y,
        }

    def get_tags(self, obj: Annotation) -> dict:
        return obj.tags.values_list("tag", flat=True)

    def get_relations(self, obj: Annotation) -> dict:
        return {"type": obj.type, "label_id": obj.parent_id}

    def get_meta(self, obj: Annotation) -> dict:
        return {
            "confirmed": obj.confirmed,
            "confidence_percent": obj.confidence_percent,
        }
