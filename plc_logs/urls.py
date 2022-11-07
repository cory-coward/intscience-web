from django.urls import path

from .views import current_well_logs, current_air_stripper_logs, set_pump_mode

app_name = 'plc_logs'
urlpatterns = [
    path('current-well-logs/', current_well_logs, name='current-well-logs'),
    path('current-air-stripper-logs/', current_air_stripper_logs, name='current-air-stripper-logs'),
    path('set-pump-mode/', set_pump_mode, name='set-pump-mode'),
]
