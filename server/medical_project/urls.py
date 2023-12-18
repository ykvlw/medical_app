from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from medical_project.router import router

schema_view = get_schema_view(
    openapi.Info(
        title="Medical App API",
        default_version="v1",
        description="API documentation for My App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),  # URL to obtain a token
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
]
