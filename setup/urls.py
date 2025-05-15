from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def favicon(request):
    return HttpResponse(status=204)


schema_view = get_schema_view(
    openapi.Info(
        title="API DRF School",
        default_version='v1',
        description="API Rest API for use in Alura's course Django Rest Framework.",
        terms_of_service="#",
        contact=openapi.Contact(email="jeff@drf-school.alura.com.br"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('manager/', admin.site.urls),
    path('school/', include('school.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('favicon.ico', favicon),  # Get ride browser (automatic) requisition for favicon
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
