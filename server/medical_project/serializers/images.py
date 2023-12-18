from rest_framework import serializers

from core.views import BaseSchemaMixin
from medical_project.models import ImageFile


class GetImageSerializer(BaseSchemaMixin, serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ["id", "image", "annotation", "created_at"]
