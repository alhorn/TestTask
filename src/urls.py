from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from rest_framework import permissions

from src.openapi import schema_generator_cls
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation",
        contact=openapi.Contact(email="alexeypushilov@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=schema_generator_cls(
        excluded_paths=[]
    )
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('', admin.site.urls),
]
