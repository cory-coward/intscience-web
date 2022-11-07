from django.urls import path

from .views import current_alarms

app_name = 'plc_alarms'
urlpatterns = [
    path('current-alarms/', current_alarms, name='current-alarms'),
]
