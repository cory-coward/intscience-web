from django.urls import path

from .views import current_well_logs, set_well_state

app_name = 'plc_logs'
urlpatterns = [
    path('current-well-logs/', current_well_logs, name='current-well-logs'),
    path('set-well-state/', set_well_state, name='set-well-state'),
]
