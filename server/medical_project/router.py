from rest_framework.routers import DefaultRouter

from medical_project.views import (
    AnnotationExternalViewSet,
    AnnotationInternalViewSet,
    AnnotationViewSet,
    ImageFileViewSet,
)

router = DefaultRouter()
router.register(r"images", ImageFileViewSet, basename="images")
router.register(r"annotations/internal", AnnotationInternalViewSet, basename="annotations_internal")
router.register(r"annotations/external", AnnotationExternalViewSet, basename="annotations_external")
router.register(r"annotations", AnnotationViewSet, basename="annotations")
