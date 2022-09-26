from django.urls import path

from .views import MaintenanceLogListView, MaintenanceLogDetailView, MaintenanceLogCreateView,\
    GardnerDenverLogListView, GardnerDenverLogDetailView, GardnerDenverLogCreateView

app_name = 'maintenance_logs'
urlpatterns = [
    path('maintenance-logs/', MaintenanceLogListView.as_view(), name='maintenance-logs'),
    path('maintenance-logs/<int:pk>/', MaintenanceLogDetailView.as_view(), name='maintenance-log-detail'),
    path('maintenance-logs/add/', MaintenanceLogCreateView.as_view(), name='create-maintenance-log'),
    path('gardner-denver-logs/', GardnerDenverLogListView.as_view(), name='gardner-denver-logs'),
    path('gardner-denver-logs/<int:pk>/', GardnerDenverLogDetailView.as_view(), name='gardner-denver-log-detail'),
    path('gardner-denver-logs/add/', GardnerDenverLogCreateView.as_view(), name='create-gardner-denver-log'),
]
