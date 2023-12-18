import django_filters

from medical_project.models import Annotation


class AnnotationFilterset(django_filters.FilterSet):
    image_file_id = django_filters.NumberFilter(required=True)

    class Meta:
        model = Annotation
        fields = ()
