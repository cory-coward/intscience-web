from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('logs/', include('maintenance_logs.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/well-logs/', include('plc_logs.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
