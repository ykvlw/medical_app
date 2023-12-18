from django.db.models import Q
from rest_framework import mixins, viewsets

from core.views import BaseViewMixin
from medical_project.filters import AnnotationFilterset
from medical_project.models import Annotation
from medical_project.schemas import AnnotationUpdateSchema
from medical_project.serializers import (
    AnnotationSerializer,
    ExternalFormatSerializer,
    InternalFormatSerializer,
)


class AnnotationViewSet(BaseViewMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Annotation.objects
    schema_update_class = AnnotationUpdateSchema
    serializer_class = AnnotationSerializer


class AnnotationInternalViewSet(BaseViewMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Annotation.objects
    serializer_class = InternalFormatSerializer
    filterset_class = AnnotationFilterset


class AnnotationExternalViewSet(BaseViewMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Annotation.objects.filter(Q(parent__isnull=True) & Q(confirmed=True))
    serializer_class = ExternalFormatSerializer
    filterset_class = AnnotationFilterset
