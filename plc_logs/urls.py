from django.urls import path

from .views import current_well_logs

app_name = 'plc_logs'
urlpatterns = [
    path('current-well-logs/', current_well_logs, name='current-well-logs'),
]
