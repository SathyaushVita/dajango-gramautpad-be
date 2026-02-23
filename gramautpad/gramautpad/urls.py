from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("hindu/",include('hindu.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path("hindu/", include('hindu.urls')),
#
    # Swagger UI available at root URL
#    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-root'),  # 👈 Add this line
    # Correct the Swagger URL by adding a trailing slash
#    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),     
#]

