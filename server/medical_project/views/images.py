from rest_framework import mixins, viewsets

from core.views import BaseViewMixin
from medical_project.models import ImageFile
from medical_project.schemas import UploadImageAndAnnotationSchema
from medical_project.serializers import GetImageSerializer


class ImageFileViewSet(
    BaseViewMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    schema_class = UploadImageAndAnnotationSchema
    serializer_class = GetImageSerializer
    queryset = ImageFile.objects
